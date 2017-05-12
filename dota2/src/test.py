import pprint

import dota2api

from src.common.env import get_env_value
from src.database.client import Dota2DBClient
from src.database.queries import get_tournament_ids, get_tournament_match_ids, get_match_ids

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
    # for doc in client.find_tournament({"name": "The International 2016"}, {"id": 1}):
    #     pprint.pprint(doc)
    pass

# print(len(get_tournament_ids()))
# print(len(get_tournament_match_ids()))
# print(len(get_match_ids()))

api = dota2api.Initialise()


# import json
#
# document = api.get_league_listing()
#
# for items in document.items():
#     for item in items:
#         for i in item:
#             print(i)
#             # doc = json.load(i)
#             # print(api.get_match_history(league_id=doc["leagueid"]))
#             break
#
# heroes = api.get_heroes()
#
# for hero in heroes["heroes"]:
#     print(hero)