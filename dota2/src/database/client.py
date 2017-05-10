from pymongo import MongoClient
from pymongo.errors import PyMongoError

from src.common.env import get_env_value


class Dota2DBClient(object):
    def __init__(self):
        self.__client = MongoClient(get_env_value("D2_DB_URI"))
        self.__db = self.__client[get_env_value("D2_DB_NAME")]
        self.__tournament_collection = self.__db["tournament"]
        self.__match_collection = self.__db["match"]

    def insert_tournament(self, doc_or_docs, *args, **kwargs):
        status = True

        try:
            self.__tournament_collection.insert(doc_or_docs=doc_or_docs,
                                                *args, **kwargs)
        except (PyMongoError, OverflowError) as e:
            print(e)
            status = False

        return status

    def find_tournament(self, filter, projection=None, *args, **kwargs):
        return self.__tournament_collection.find(filter=filter,
                                                 projection=projection,
                                                 *args, **kwargs)

    def insert_match(self, doc_or_docs, *args, **kwargs):
        status = True

        try:
            self.__match_collection.insert(doc_or_docs=doc_or_docs,
                                           *args, **kwargs)
        except (PyMongoError, OverflowError) as e:
            print(e)
            status = False

        return status

    def find_match(self, filter, projection=None, *args, **kwargs):
        return self.__match_collection.find(filter=filter,
                                            projection=projection,
                                            *args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        self.__client.close()
