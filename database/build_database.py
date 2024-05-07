import datetime
import uuid
import time
import config

import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey

from data_process import image_process, node_process, image_lists_process, text_process

HOST = config.settings['host']
MASTER_KEY = config.settings['master_key']
DATABASE_ID = config.settings['database_id']
DOCUMENT_CONTAINER_ID = config.settings['document_container_id']
SEARCH_CONTAINER_ID = config.settings['search_container_id']

data = {
    'metadata' : {
        'doc_id' : 'XXXX-YYYY',
        'title' : 'abcd',
        'description' : 'xxxx',
        'og-image' : '',
        },
    'url' : 'https://en.wikipedia.org/wiki/Dune_(2021_film)',
    'content' : '''
            Dune (titled onscreen as Dune: Part One) is a 2021 American epic science fiction film directed and co-produced by Denis Villeneuve, 
            who co-wrote the screenplay with Jon Spaihts, and Eric Roth. 
            It is the first of a two-part adaptation of the 1965 novel of the same name by Frank Herbert. 
            Set in the distant future, the film follows Paul Atreides as his family, the noble House Atreides, is thrust into a war for the deadly and inhospitable desert planet Arrakis. 
            The ensemble cast includes Timothée Chalamet, Rebecca Ferguson, Oscar Isaac, Josh Brolin, Stellan Skarsgård, Dave Bautista, Stephen McKinley Henderson, Zendaya, Chang Chen, Sharon Duncan-Brewster, Charlotte Rampling, Jason Momoa, and Javier Bardem.
            ''',
    'user_id' : 'andrew',
    }

data_format = {
    'id' : '12345',
    'doc_id' : '000000',
    'user_id' : 'andrew',
    'url' : 'https://en.wikipedia.org/wiki/Dune_(2021_film)',
    'title' : 'abcd',
    'description' : 'xxxx',
    'chunk_index' : '0',
    'chunk_content' : 'content.....',
    'chunk_vector' : '[1, 2, 3]'
}

def set_up():
    client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    try:
        # setup database for this sample
        try:
            db = client.create_database(id=DATABASE_ID)
            print('Database with id \'{0}\' created'.format(DATABASE_ID))

        except exceptions.CosmosResourceExistsError:
            db = client.get_database_client(DATABASE_ID)
            print('Database with id \'{0}\' was found'.format(DATABASE_ID))

        # setup container1 for this sample
        try:
            container1 = db.create_container(id=DOCUMENT_CONTAINER_ID, partition_key=PartitionKey(path='/user_id'))
            print('Container with id \'{0}\' created'.format(DOCUMENT_CONTAINER_ID))

        except exceptions.CosmosResourceExistsError:
            container1 = db.get_container_client(DOCUMENT_CONTAINER_ID)
            print('Container with id \'{0}\' was found'.format(DOCUMENT_CONTAINER_ID))
        
        # setup container2 for this sample
        try:
            container2 = db.create_container(id=SEARCH_CONTAINER_ID, partition_key=PartitionKey(path='/doc_id'))
            print('Container with id \'{0}\' created'.format(SEARCH_CONTAINER_ID))

        except exceptions.CosmosResourceExistsError:
            container2 = db.get_container_client(SEARCH_CONTAINER_ID)
            print('Container with id \'{0}\' was found'.format(SEARCH_CONTAINER_ID))
        
        return container1, container2

    except exceptions.CosmosHttpResponseError as e:
        print('\nrun_sample has caught an error. {0}'.format(e.message))

def create_items(container, data):
    '''
    Create an item in a container.
    :param container: azure.cosmos.container.ContainerProxy object
    :param data: the data you want to save, which should be in JSON format
    '''
    container.create_item(body=data)

def scale_container(container):
    print('\nScaling Container\n')
    
    # You can scale the throughput (RU/s) of your container up and down to meet the needs of the workload. Learn more: https://aka.ms/cosmos-request-units
    try:
        offer = container.read_offer()
        print('Found Offer and its throughput is \'{0}\''.format(offer.offer_throughput))

        offer.offer_throughput += 100
        container.replace_throughput(offer.offer_throughput)

        print('Replaced Offer. Offer Throughput is now \'{0}\''.format(offer.offer_throughput))
    
    except exceptions.CosmosHttpResponseError as e:
        if e.status_code == 400:
            print('Cannot read container throuthput.');
            print(e.http_error_message);
        else:
            raise;

def read_item(container, id, partition_key, target:list):
    '''
    Do an efficient point read lookup on partition key and id.
    :param container:
    :param id: id of the ducument/chunk
    :param partition_key: the partition key, which is user_id here
    :param target: a list that contains the feature you want to query
    :return: a dictionary that contains the 
    '''
    answer = {'ID': id}
    # We can do an efficient point read lookup on partition key and id
    response = container.read_item(item=id, partition_key=partition_key)
    for t in target:
        answer[t] = response.get(t)
    return answer


def read_items(container):
    # NOTE: Use MaxItemCount on Options to control how many items come back per trip to the server
    #       Important to handle throttles whenever you are doing operations such as this that might
    #       result in a 429 (throttled request)
    item_list = list(container.read_all_items(max_item_count=10))

    print('Found {0} items'.format(item_list.__len__()))

    for doc in item_list:
        print('Id: {0}'.format(doc.get('id')))


def query_items(container, partition_key, query, parameters):
    print('\nQuerying for an Item by Partition Key\n')

    # Including the partition key value of account_number in the WHERE filter results in a more efficient query
    # items = list(container.query_items(
    #     query="SELECT * FROM r WHERE r.partitionKey=@account_number",
    #     parameters=[
    #         { "name":"@account_number", "value": partition_key }
    #     ]
    # ))
    items = list(container.query_items(
        query=query,
        parameters=[parameters]
    ))
    print('Item queried by Partition Key {0}'.format(items[0].get("id")))


def replace_item(container, doc_id, partition_key):
    read_item = container.read_item(item=doc_id, partition_key=partition_key)
    read_item['subtotal'] = read_item['subtotal'] + 1
    response = container.replace_item(item=read_item, body=read_item)

    print('Replaced Item\'s Id is {0}, new subtotal={1}'.format(response['id'], response['subtotal']))


def upsert_item(container, doc_id, partition_key):
    print('\nUpserting an item\n')

    read_item = container.read_item(item=doc_id, partition_key=partition_key)
    read_item['subtotal'] = read_item['subtotal'] + 1
    response = container.upsert_item(body=read_item)


def delete_item(container, doc_id, partition_key):
    print('\nDeleting Item by Id\n')

    response = container.delete_item(item=doc_id, partition_key=partition_key)

def get_containers():
    client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
    db = client.get_database_client(DATABASE_ID)
    container1 = db.get_container_client(DOCUMENT_CONTAINER_ID)
    container2 = db.get_container_client(SEARCH_CONTAINER_ID)
    return container1, container2

def input_process(data):
    input_data = {}
    metadata = data['metadata']
    input_data['id'] = metadata['doc_id']
    input_data['url'] = data['url']
    input_data['title'] = metadata['title']
    input_data['description'] = metadata['description']
    input_data['og-image'] = metadata['og-image']
    input_data['content'] = data['content']
    input_data['user_id'] = data['user_id']
    input_data['summary_title'] = ''
    input_data['summary'] = ''
    return input_data

def chunk_save(container, input_data):
    content = input_data['content']
    nodes = node_process(content)
    node_contents = nodes['contents']
    node_embeddings = nodes['embeddings']
    for i, content in enumerate(node_contents):
        search_data = {}
        search_data['id'] = str(uuid.uuid4())
        search_data['doc_id'] = input_data['id']
        search_data['user_id'] = input_data['user_id']
        search_data['url'] = input_data['url']
        search_data['title'] = input_data['title']
        search_data['description'] = input_data['description']
        search_data['chunk_index'] = str(i)
        search_data['chunk_content'] = content
        search_data['chunk_vector'] = node_embeddings[i]
        create_items(container, search_data)

def document_save(doc_container, chunk_container, data):
    input_data = input_process(data)
    create_items(doc_container, input_data)
    chunk_save(chunk_container, input_data)

# #Set up the two containers
# document_container, search_data_container = set_up()

# #Get the two containers
# document_container, search_data_container = get_containers()

# #Save document
# document_save(document_container, search_data_container, data)

# #Read all the items in the container
# read_items(document_container)
# read_items(search_data_container)

# #Get specific data in containers
# print(read_item(search_data_container, '2d09f175-af17-404d-b21f-abfce67a7b25', 'XXXX-YYYY', ['chunk_index', 'chunk_content']))
