from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from src.common.env import get_env_value


class Dota2DBClient(object):
    def __init__(self):
        self.client = MongoClient(get_env_value("D2_DB_URI"))
        self.db = self.client[get_env_value("D2_DB_NAME")]
        self.tournament_collection = self.db[get_env_value("D2_DB_COLLECTION_TOURNAMENT")]
        self.match_collection = self.db[get_env_value("D2_DB_COLLECTION_MATCH")]

    def insert_tournament(self, doc_or_docs):
        status = True

        try:
            self.tournament_collection.insert(doc_or_docs=doc_or_docs)
        except DuplicateKeyError:
            status = False

        return status

    def find_tournament(self, filter, projection=None):
        return self.tournament_collection.find(filter=filter,
                                               projection=projection)

    def insert_match(self, doc_or_docs):
        status = True

        try:
            self.match_collection.insert(doc_or_docs=doc_or_docs)
        except DuplicateKeyError:
            status = False

        return status

    def find_match(self, filter, projection=None):
        return self.match_collection.find(filter=filter,
                                          projection=projection)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        self.client.close()
