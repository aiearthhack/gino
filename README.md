<p align="center"><img src="https://github.com/aiearthhack/gino/blob/main/logo2.png"></p>


## Inspiration
We are a team of passionate GenAI enthusiasts and classmates from the University of Washington. We are inspired to build products that address our shared frustration. 
We found ourselves overwhelmed by messy "read-it-later" lists, scattered saved content, and lost insights. Moreover, most information online is confined to a single format. However, we learn best in different ways and situations. We craved more digestible knowledge formats to match our busy lives.
Other than four of us who suffer the pain, we interviewed eight classmates and five tech professionals, and we confirmed we weren't alone.
Guided by a comprehensive product roadmap, we are committed to expanding the product together.

## What it does
Gino.AI empowers you to capture articles, images, and more, transforming them into customized summaries and personalized podcasts that fit your unique learning style. No more scattered insights or forgotten valuable content.
Moreover, with the powerful 'Ask Me!' assistant chatbot, you won't get lost in scattered information anymore. Simply ask questions and interact to get insights whenever you need them from your centralized knowledge management system - Mind Base, where you can store and organize your knowledge.
Whether you're a visual learner who thrives on summaries, an auditory learner who loves podcasts, a kinesthetic learner who needs to interact with information, or someone who enjoys a blend of all three, depending on the situation, Gino.AI has you covered.
## Key Features <br>
**1. Universal Knowledge Capture**:  Gino.AI provides multi-modal content capture, which can capture articles, news, and even images and files that fuel your curiosity – no matter the format.  
**2. Smart Summary**:  Transform long contexts into concise summaries to grasp key points quickly. You can even customize it based on your needs!  
**3. Personalized Podcast**:
Knowledge on the go - turns your saved content into digestible audio podcasts.  
**4. Ask Me! - Knowledge Assistant**:
Interact with your knowledge space with simple questions to retrieve information and insights.  
**5. Mind Base—Your Knowledge Space**:
This is your centralized, searchable knowledge space, where you store and organize your content, ensuring easy access whenever you need it.  

## How we built it
Gino.AI leverages combined Azure Services and modern web technologies to create robust and trustworthy tools for our users. <br>
### Solution Architecture: <br>
![architecture](https://github.com/aiearthhack/gino/blob/main/Gino.AI%20general.png)
### Core Azure solutions:
* Azure AI Vision: Analyze and extract text from images. (OCR and Clip models embedding)<br>
* Azure AI Search: search service for indexing and efficient querying from Mind Base knowledge base data.<br>
* Azure AI Document Intelligence: Accurately extract PDF content, including text, key-value pairs, tables, and structures, from documents.<br>
* Azure Cosmos PostgreSQL: Store structured data. <br>
* Azure Cosmos DB NonSQL: Store unstructured data, including embeddings.<br>
* OpenAI GPT-4: Cutting-edge LLM is used to generate personalized summaries and podcast scripts and for chatbots to analyze user input and generated responses.<br>
* Azure AI Content Safety: Filter harmful content for RAG chatbot, summaries, and podcast scripts, ensuring responsible AI.
### Universal Knowledge Capture:
![architecture](https://github.com/aiearthhack/gino/blob/main/Gino.AI_%20Capture.png)
In our system, the knowledge capture flow initiates on the front-end, allowing users to input content through various methods including URL text input, image upload, or our Chrome plugin. Users can add multiple captures to a staging area known as "Studio". From this point, the captured content is processed using Azure AI OCR and Document Intelligence to extract meaningful information.

Once the data is captured and processed on the front-end, it is transmitted to the back-end where we utilize Cosmos DB for NoSQL as our database solution. We have established a database and configured two containers: 'Document', dedicated to storing documents, and 'Search', which holds chunks that are further utilized for Azure AI search. Upon receiving the ParseHTML input from the front-end, we employ LlamaIndex for text splitting and text-embedding-3-small for text embedding, ensuring effective data handling and retrieval.
### Smart Summary:
![architecture](https://github.com/aiearthhack/gino/blob/main/Gino.AI_summary.png)
For summarization, we selected GPT-4-turbo due to its impressive context window size of 128,000. We also enable users to customize their summaries, including adjusting the length and format. Upon receiving a user request for summarization, we generate the summary and update it in the database.

### Personalized Podcast:
![architecture](https://github.com/aiearthhack/gino/blob/main/Gino.AI_podcast.png)
To create a hyper-personalized podcast, we leveraged textual content and expertly crafted prompts for the Azure OpenAI Service, enabling the generation of highly relevant and engaging podcast content. Finally, we employed Azure Text to Speech to deliver a narrative experience that closely mimics human speech.

### Retrieval-augmented generation (RAG):
![architecture](https://github.com/aiearthhack/gino/blob/main/Gino.AI_RAG.png)
Users can save articles into their personal MindBase, and our Retrieval Augmented Generation (RAG) chatbot enables users to interact with all the knowledge stored in their MindBase. Users can ask questions or chat with the MindBase assistant to learn more details about the saved content. To maintain accuracy and reduce hallucination, we use Azure Cognitive Search as our primary retrieval tool, utilizing both vector and full-text search to find relevant pieces of information. All entries in the Azure Cosmos DB NoSQL database are automatically indexed in Azure Cognitive Search.

If there are questions that the assistant finds difficult to answer using only the information from the user's MindBase, it will ask the user for permission to use external internet search tools to find additional relevant knowledge. When providing answers, the assistant will include sources and links, allowing users to confirm the information's accuracy.
To further enhance the user experience, we plan to make the chat history searchable and accessible. In the near future, we intend to store the chat history in an Azure Cosmos DB for PostgreSQL database, enabling users to easily retrieve and review previous conversations with the MindBase assistant.

## What's next for Gino.AI
### Phase 1: User Experience and Core Functionality<br>
* Robust Website: Utilize React to build an engaging and user-friendly web experience. Implement our draft web UI designed.  (see image below)<br>
* Expand Content Capture: <br>
  **1. Chat App Integration**: Integrate with WhatsApp to streamline content capture, meeting the needs of users who save article links within their familiar chat app. <br>
  **2. Chrome Extension**: Develop a seamless web clipping tool to capture content directly within Chrome for a frictionless user experience.  <br>
* Optimize User Experience: Gather feedback from 10 users on the minimum viable product to optimize the user flow.  <br>
### Phase 2: Enhanced Features and Multimodal Expansion<br>
* Podcast Customization: Introduce customizable podcast settings, such as voice and speed, to cater to individual preferences.  <br>
* Multimodal Expansion to Video: Expand content capture and processing capabilities to include video content.  <br>
* Customizable Newsletters: Empower users to create tailored summaries in their preferred newsletter format for efficient knowledge intake.  <br>
### Phase 3: Mobile Application and Social Sharing <br>
* iOS App Development: Launch a native iOS application to provide users with a seamless mobile experience.  <br>
* Social Sharing: Facilitate easy sharing of summaries, newsletters, and podcasts, encouraging knowledge engagement and collaboration among users.  <br>

## What We learned: 
1. Hands-on exploring Azure AI service development and integration. <br>
2. Customer-centric mindset: UI/UX design impacts the whole solution design, such as data storage and data pipeline. We learned to prioritize the most essential data points and present them clearly and accessiblely. <br>
