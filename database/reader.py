from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import (
    SentenceSplitter,
    SemanticSplitterNodeParser,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core.response.notebook_utils import display_source_node
import os
import json
from tempfile import TemporaryFile, NamedTemporaryFile

def SimpleTextReader(text):
    '''
    This function aims to read a piece of text with type str.
    :param text: the text that user want to read.
    :return: a 'llama_index.core.schema.Document' object.
    '''
    with NamedTemporaryFile('w+t') as f:
        f.write(text)
        f.seek(0)
        documents = SimpleDirectoryReader(input_files=[f.name]).load_data()
    return documents

def contentReader(mode, file_path = '', text = ''):
    '''
    This function aims to read the content with different types, including file and str.
    :param mode: 'directory reader' or 'text reader'. If 'directory reader' was chosen, user must provide the file path. If 'text reader' was chosen, user must provide the text.
    :param file_path: the directory of the file that user want to read.
    :param text: the text that user want to read.
    :return: a list of 'llama_index.core.schema.Document' object.
    '''
    if mode == 'directory reader':
        documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
    elif mode == 'text reader':
        documents = SimpleTextReader(text)
    return documents

def documentProcess(documents):
    '''
    This function aims to split the documents into different chunks return the nodes.
    :param documents: the documents that user want to deal with.
    :return: a list of 'llama_index.core.schema.TextNode' object.
    '''
    embed_model = OpenAIEmbedding()
    splitter = SemanticSplitterNodeParser(
        buffer_size=1, breakpoint_percentile_threshold=95, embed_model=embed_model
    )
    nodes = splitter.get_nodes_from_documents(documents)
    return nodes

# documents = contentReader(mode = 'directory reader', file_path = "稿子.txt")
# nodes = documentProcess(documents)
# node = nodes[0].to_json()
# node = json.loads(node)
# print(node['excluded_llm_metadata_keys'])
# print(node['text'])
# print(node['metadata']['creation_date'])