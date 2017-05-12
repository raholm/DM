import pprint

from src.util.date import timestamp_to_readable
from src.util.env import get_env_value
from src.database.client import Dota2DBClient
from src.database.queries import get_tournament_ids, get_tournament_match_ids, get_match_ids, get_picks_bans, \
    get_time_frame

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

with Dota2DBClient() as client:
    # print(get_picks_bans(client, 2569531910))
    # print(get_picks_bans(client, 2569415435))
    # print(get_picks_bans(client, [2569531910, 2569415435]))
    times = get_time_frame(client, "The International 2014")
    for time in times:
        print(timestamp_to_readable(time))
