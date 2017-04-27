import pprint

from src.common.env import get_env_value
from src.database.client import Dota2DBClient

print(get_env_value("D2_DB_URI"))
print(get_env_value("D2_DB_NAME"))
print(get_env_value("D2_DB_COLLECTION_TOURNAMENT"))
print(get_env_value("D2_DB_COLLECTION_MATCH"))

with Dota2DBClient() as client:
    # for doc in client.tournament_collection.find({}, {"name": 1}):
    #     pprint.pprint(doc)
    #
    # for doc in client.tournament_collection.find({"name": "The International 2016"}):
    #     pprint.pprint(doc)
    # for doc in client.find_tournament({"name": "The International 2016"}):
    #     pprint.pprint(doc)
    #
    # for doc in client.find_tournament({}, {"name": 1}):
    #     pprint.pprint(doc)
    #
    # for doc in client.find_tournament({"name": "The International 2016"}, {"name": 1}):
    #     pprint.pprint(doc)