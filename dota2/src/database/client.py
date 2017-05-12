from pymongo import MongoClient
from pymongo.errors import PyMongoError

from src.common.env import get_env_value


class Dota2DBClient(object):
    valid_collections = ["tournament", "match", "item", "hero", "ability"]

    def __init__(self):
        self.__client = MongoClient(get_env_value("D2_DB_URI"))
        self.__db = self.__client[get_env_value("D2_DB_NAME")]

    def insert(self, doc_or_docs, collection, *args, **kwargs):
        self.__check_collection(collection)

        status = True

        try:
            dbcollection = self.__db[collection]
            dbcollection.insert(doc_or_docs=doc_or_docs, *args, **kwargs)
        except (PyMongoError, OverflowError) as e:
            print(e)
            status = False

        return status

    def find(self, collection, filter, projection=None, *args, **kwargs):
        self.__check_collection(collection)
        collection = self.__db[collection]
        return collection.find(filter=filter, projection=projection,
                               *args, **kwargs)

    def insert_tournament(self, doc_or_docs, *args, **kwargs):
        return self.insert(doc_or_docs, "tournament", *args, **kwargs)

    def find_tournament(self, filter, projection=None, *args, **kwargs):
        return self.find(collection="tournament",
                         filter=filter,
                         projection=projection,
                         *args, **kwargs)

    def insert_match(self, doc_or_docs, *args, **kwargs):
        return self.insert(doc_or_docs, "match", *args, **kwargs)

    def find_match(self, filter, projection=None, *args, **kwargs):
        return self.find(collection="match",
                         filter=filter,
                         projection=projection,
                         *args, **kwargs)

    def __check_collection(self, collection):
        if not isinstance(collection, str) and \
                        collection not in self.valid_collections:
            raise ValueError("Invalid collection: %s" % (collection,))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        self.__client.close()
