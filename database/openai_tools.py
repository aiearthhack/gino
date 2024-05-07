import os
import base64
import requests
import openai
from openai import OpenAI

# OpenAI API Key
api_key = os.environ['OPENAI_API_KEY']
client = OpenAI()

def chatGPT(user_prompt:str, system_prompt: str, temperature: float, max_tokens: int, document:str='')->str:
    completion = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": f"This is the document: {document}"},
        {"role": "user", "content": f"{user_prompt}"}
    ],
    temperature = temperature,
    max_tokens = max_tokens,
    )
    response = completion.choices[0].message.content
    return response

def summarization(document, length, format, system_prompt):
    temperature = 1
    if length == 'short':
        max_tokens = 50
        system_prompt += ' Your answer should be breif enough to guarantee that the output tokens are less than 50.'
    elif length == 'medium':
        max_tokens = 100
        system_prompt += ' Your answer should be in moderate length with the output tokens less than 100 but larger than 50.'
    elif length == 'long':
        max_tokens = 250
        system_prompt += ' Your answer should be long enough with the output tokens less than 250 but larger than 100.'
    if format == 'paragraph':
        answer_format = 'Your answer should be writen in paragraphs. You can not use bullet point.'
    elif format == 'bullet':
        answer_format = '''
        Your answer should be listed bullet point like this 
        'Summary:
        •<Write your summary here>
        •<Write your summary here>'
        '''
    user_prompt = answer_format
    summary = chatGPT(user_prompt, system_prompt, temperature, max_tokens)
    return summary
# do summarization
def summary_assistant(document_list, length, format):
    summary_list = []
    for i, doc in enumerate(document_list):
        system_prompt1 = f'''
            This is the content from a webpage {doc}.
            Please do summarization for the content of the current webpage.
            '''
        summary = summarization(doc, length, format, system_prompt1)
        summary_list.append(f'The summary of webpage {i} is: ' + summary)
    summaries =  '\n'.join(summary_list)
    system_prompt2 = f'''
    These are the summaries from several webpages: {summaries}.
    Please combine these summaries together and summarize all if them.
    '''
    final_summary = summarization(doc, length, format, system_prompt2)
    return final_summary
    
# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  
def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

# Path to your image
def image2text_by_path(image_path):
    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-turbo",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "What’s in this image?"
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    content = response.json()['choices'][0]['message']['content']
    return content

def image2text_by_url(url):
    response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "What’s in this image?"},
            {
            "type": "image_url",
            "image_url": {
                "url": url,
            },
            },
        ],
        }
    ],
    max_tokens=300,
    )

    content = response.choices[0].message.content
    return content
