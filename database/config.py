import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://gino-database.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', 'm3p8JVU4DAxU5NbRHwp54GAaMdEzzMrILyOJK001IBdvkwo68y6gbWtytuXP3dZHn8NQB0A7CD5BACDbCDmd3Q=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'Database'),
    'document_container_id': os.environ.get('COSMOS_CONTAINER', 'Document'),
    'search_container_id': os.environ.get('COSMOS_CONTAINER', 'Search'),
}
