import json
import os
from typing import Dict, List

import requests
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.callbacks import LangChainTracer
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain.tools import StructuredTool
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.chat_models import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tools import ToolException
from langchain_openai import ChatOpenAI
from langsmith import Client
from openai import OpenAI

load_dotenv(override=True)


def generate_embeddings(text):
    """
    Generate embeddings for the given text using OpenAI API.
    Latest model "text-embedding-3-small" returns 1536-dimensional embeddings.
    """

    api_key = os.getenv("openai_api_key")
    client = OpenAI(api_key=api_key)
    model = os.getenv("openai_embeddings")

    try:
        text = text.replace("\n", " ")
        return client.embeddings.create(input=[text], model=model).data[0].embedding
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return None


def hybrid_search(query, user_id, index_name="gino-vector-search-index"):
    ai_search_endpoint = os.getenv("cognitive_search_endpoint")
    ai_search_api_key = os.getenv("cognitive_search_api_key")

    endpoint = (
        f"{ai_search_endpoint}/indexes/{index_name}/docs/search?api-version=2023-11-01"
    )

    headers = {"Content-Type": "application/json", "api-key": ai_search_api_key}

    payload = {
        "vectorQueries": [
            {
                "vector": generate_embeddings(query),
                "fields": "para_vector",
                "kind": "vector",
                "k": 15,
            }
        ],
        "search": query,
        "searchFields": "title,para_content",
        "select": "doc_id, title, url, para_index, para_content",
        "filter": f"user_id eq '{user_id}'",
        "vectorFilterMode": "preFilter",
        "top": "10",
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload)

        if response.status_code == 200:
            results = response.json()
            return parse_search_results(results)
        else:
            print(
                f"Error performing hybrid search. Status code: {response.status_code}"
            )
            print(f"Error message: {response.text}")

    except Exception as e:
        print("Error performing hybrid search:", e)

    return None


def parse_search_results(results):
    search_results = []
    for item in results["value"]:
        search = {
            "doc_id": item["doc_id"],
            "title": item["title"],
            "url": item["url"],
            "para_index": item["para_index"],
            "para_content": item["para_content"],
        }
        search_results.append(search)
    return search_results


def _handle_error(error: ToolException) -> str:
    return (
        "The following errors occurred during tool execution:"
        + error.args[0]
        + "Please try another tool."
    )


# Define the tool using LangChain StructuredTool dataclass
def hybrid_search_tool(query: str, user_id: str) -> List[Dict]:
    return hybrid_search(query, user_id)


HybridSearchTool = StructuredTool.from_function(
    name="HybridSearchTool",
    description="Performs a hybrid search using the Gino vector search index.",
    func=hybrid_search_tool,
    handle_tool_error=_handle_error,
)


class AgentManger:
    def __init__(self, config_path="config.json"):
        with open(config_path, "r") as f:
            self.config = json.load(f)

        # LangSmith Configurations
        self.callbacks = [
            LangChainTracer(
                project_name=os.getenv("LANGCHAIN_PROJECT"),
                client=Client(
                    api_url="https://api.smith.langchain.com",
                    api_key=os.getenv("LANGCHAIN_API_KEY"),
                ),
            )
        ]

        self.llm = ChatOpenAI(
            api_key=os.getenv("openai_api_key"),
            temperature=self.config.get("chat_temperature"),
            model_name=self.config.get("chat_model"),
        )
        self.tools = [HybridSearchTool, TavilySearchResults()]
        self.chat_agent = self.create_agent(
            instruction=self.config.get("chat_instruction")
        )

        # logging.basicConfig(
        #     filename='./logs/conversation_logs.log',
        #     level=logging.INFO,
        #     format='%(asctime)s - %(message)s',
        #     filemode='a'
        # )
        # print("Logging setup complete.")

    # def log_message(self, session_id, user_id, user_message, assistant_response):
    #     log_entry = {
    #         'session_id': session_id,
    #         'user_id': user_id,
    #         'user_message': user_message,
    #         'assistant_response': assistant_response,
    #         'timestamp': datetime.now().isoformat()
    #     }
    #     print("Logging entry:", log_entry)  # Check the log entry content
    #     logging.info(json.dumps(log_entry))
    #     print("Log entry written.")

    def create_agent(self, instruction):
        """
        Create an agent that uses the OpenAI language model and the specified tools.

        Args:
            llm (ChatOpenAI): The language model to use.
            tools (List[BaseTool]): The tools to use.
            prompt (ChatPromptTemplate): The prompt to use.

        Returns:
            Agent: The created agent.
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(instruction),
                MessagesPlaceholder(variable_name="chat_history", optional=True),
                HumanMessagePromptTemplate.from_template("{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        print(prompt)

        agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

        # add history to the agent
        message_history = ChatMessageHistory()
        agent_with_chat_history = RunnableWithMessageHistory(
            agent_executor,
            lambda session_id: message_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        return agent_with_chat_history

    def chat_with_agent(self, input_message, session_id, user_id):
        """ """
        result = self.chat_agent.invoke(
            {"input": f"user_id: {user_id}\n user: {input_message}"},
            config={
                "configurable": {"session_id": session_id},
                "callbacks": self.callbacks,
            },
        )

        # # Log the conversation
        # self.log_message(session_id, user_id, input_message, result)

        return result


## Initialize the agent manager
rag_agent = AgentManger()


## Create a chat function for application to use
def chat(user_message, session_id, user_id):
    return rag_agent.chat_with_agent(user_message, session_id, user_id)
