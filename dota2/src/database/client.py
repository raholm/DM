from pymongo import MongoClient
from pymongo.errors import PyMongoError

from src.util.env import get_env_value


class Dota2DBClient(object):
    valid_collections = ["league", "match", "hero", "item"]
    uri = get_env_value("D2_DB_URI")
    db_name = get_env_value("D2_DB_NAME")

    def __init__(self):
        self.__client = MongoClient(self.uri)
        self.__db = self.__client[self.db_name]

    def insert(self, collection, doc_or_docs, *args, **kwargs):
        self.__check_collection(collection)

        status = True

        try:
            collection = self.__db[collection]
            collection.insert(doc_or_docs=doc_or_docs,
                              *args, **kwargs)
        except (PyMongoError, OverflowError) as e:
            print(e)
            status = False

        return status

    def find(self, collection, filter, projection=None, *args, **kwargs):
        self.__check_collection(collection)

        collection = self.__db[collection]
        return collection.find(filter=filter, projection=projection,
                               *args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        self.__client.close()

    def __check_collection(self, collection):
        if not isinstance(collection, str) and \
                        collection not in self.valid_collections:
            raise ValueError("Invalid collection: %s" % (collection,))
