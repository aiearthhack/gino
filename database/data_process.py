from azure_AI import abstractive_summarization, keywords_extraction
from openai_tools import get_embedding, image2text_by_url
from reader import contentReader, documentProcess
import json

text = '''
Before college the two main things I worked on, outside of school, were writing and programming. I didn't write essays. I wrote what beginning writers were supposed to write then, and probably still are: short stories. My stories were awful. They had hardly any plot, just characters with strong feelings, which I imagined made them deep.
The first programs I tried writing were on the IBM 1401 that our school district used for what was then called "data processing." This was in 9th grade, so I was 13 or 14. The school district's 1401 happened to be in the basement of our junior high school, and my friend Rich Draves and I got permission to use it. It was like a mini Bond villain's lair down there, with all these alien-looking machines — CPU, disk drives, printer, card reader — sitting up on a raised floor under bright fluorescent lights.
The language we used was an early version of Fortran. You had to type programs on punch cards, then stack them in the card reader and press a button to load the program into memory and run it. The result would ordinarily be to print something on the spectacularly loud printer.
I was puzzled by the 1401. I couldn't figure out what to do with it. And in retrospect there's not much I could have done with it. The only form of input to programs was data stored on punched cards, and I didn't have any data stored on punched cards. The only other option was to do things that didn't rely on any input, like calculate approximations of pi, but I didn't know enough math to do anything interesting of that type. So I'm not surprised I can't remember any programs I wrote, because they can't have done much. My clearest memory is of the moment I learned it was possible for programs not to terminate, when one of mine didn't. On a machine without time-sharing, this was a social as well as a technical error, as the data center manager's expression made clear.
With microcomputers, everything changed. Now you could have a computer sitting right in front of you, on a desk, that could respond to your keystrokes as it was running instead of just churning through a stack of punch cards and then stopping.
'''

def image_process(url)->dict:
    '''
    Given the image url, extract the content of the image, and do summarization, keywords extraction
    :param url: the url of the image
    :return: a dictionary that contains the content, content embedding, keywords, keywords embedding, and url of the image
    content:str, the content of the image
    content embedding:str, the embedding of the summary of the image, which is a list of str.
    keywords:list, a list that contains the keywords of the image, e.g. ['car', 'Japan'].
    keywords embedding:list[list], the embedding of the keywords of the image, which is a list that contains lists of keywords embeddings. e.g. if keywords = ['car', 'Japan'], then keywords_embedding = [list1, list2] where list1 and list2 are the embedding vectors of 'car' and 'Japan' respectively.
    '''
    #First, extract the info from an image
    content = image2text_by_url(url)

    # #Get the summary of the content
    # summary = abstractive_summarization([content])[0]

    #Get the keywords of the content
    keywords = keywords_extraction([content])[0]

    #Get the embedding of the summary and keywords
    content_embedding = get_embedding(content)
    keywords_embedding = [get_embedding(k) for k in keywords]

    image_json =  {
        'content' : content,
        'content embedding': content_embedding,
        'keywords' : keywords,
        'keywords embedding' : keywords_embedding,
        'url' : url
        }
    return image_json

def image_lists_process(image_url_list:list):
    content = []
    content_embedding = []
    keywords = []
    keywords_embedding = []
    Url = []
    for url in image_url_list:
        Url.append(url)
        image_json = image_process(url)
        content.append(image_json['content'])
        content_embedding.append(image_json['content embedding'])
        keywords.append(image_json['keywords'])
        keywords_embedding.append(image_json['keywords embedding'])

    image_list_json = {
        'content' : content,
        'content embedding': content_embedding,
        'keywords' : keywords,
        'keywords embedding' : keywords_embedding,
        'url' : Url
    }
    return image_list_json

def node_process(text):
    documents = contentReader(mode = 'text reader', text = text)
    nodes = documentProcess(documents)
    embeddings = []
    contents = []
    for node in nodes:
        #get the node
        node = nodes[0].to_json()
        node = json.loads(node)

        #get the node information
        node_content = node['text']
        contents.append(node_content)
        nodes_metadata_keys = node['excluded_llm_metadata_keys']
        node_metadata = node['metadata']

        #get the content embedding
        text_embedding = get_embedding(node_content)
        embeddings.append(text_embedding)

    nodes_json = {
            'metadata' : node_metadata,
            'nodes metadata keys' : nodes_metadata_keys,
            'contents' : contents,
            'embeddings' : embeddings
        }
    return nodes_json

def text_process(text):
    '''
    Given the text, do summarization, keywords extraction, text spliting, and vectorize these contents.
    :param text: content of the text
    :return: a dictionary that contains the summary, summary embedding, keywords, keywords embedding, the raw text, and the nodes information of the chunks after splitting. 
    '''
    #Get the summary of the content
    summary = abstractive_summarization([text])[0]

    #Get the keywords of the content
    keywords = keywords_extraction([text])[0]

    #Get the embedding of the text, summary, and keywords
    nodes = node_process(text)
    summary_embedding = get_embedding(summary)
    keywords_embedding = [get_embedding(k) for k in keywords]
    text_json =  {
        'summary': summary,
        'summary_embedding': summary_embedding,
        'keywords' : keywords,
        'keywords_embedding': keywords_embedding,
        'content' : text,
        'nodes' : nodes
        }
    return text_json

# url1 = "https://upload.wikimedia.org/wikipedia/zh/a/a1/Dune_Part_Two_Poster.jpg"
# url2 = "https://upload.wikimedia.org/wikipedia/zh/a/a1/Dune_Part_Two_Poster.jpg"

# image_json = image_process(url)
# print(image_json.keys())
# print(len(image_json['keywords embedding']))

#text_process('The dataset contains a total of 568,454 food reviews Amazon users left up to October 2012. We will use a subset of 1,000 most recent reviews for illustration purposes. The reviews are in English and tend to be positive or negative. Each review has a ProductId, UserId, Score, review title (Summary) and review body (Text). For example:')
#node_process(text)
# text_json = text_process(text)

# image_list = [url1, url2]
# image_list_json = image_lists_process(image_list)
# print(image_list_json.keys())
# print(len(image_list_json['content']))
# print(image_list_json['url'])

