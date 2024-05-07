import os
from dotenv import load_dotenv

from azure.cosmos import CosmosClient

from config_consts import COSMOSDB_URI, COSMOSDB_KEY, COSMOSDB_DATABASE_NAME

load_dotenv(override=True)


class CosmosDBClient:
    def __init__(self):
        self.url = os.environ.get(COSMOSDB_URI)
        self.key = os.environ.get(COSMOSDB_KEY)
        self.database_name = os.environ.get(COSMOSDB_DATABASE_NAME)

        self._client = None

    def _get_client(self):
        if self._client is None:
            self._client = CosmosClient(self.url, self.key)
        return self._client

    def get_database(self):
        return self._get_client().get_database_client(self.database_name)

    def get_container(self, container_name):
        database = self.get_database()
        return database.get_container_client(container_name)
