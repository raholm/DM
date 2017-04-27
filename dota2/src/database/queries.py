from src.database.client import Dota2DBClient


def get_tournament_ids():
    with Dota2DBClient() as client:
        ids = [doc["id"] for doc in client.find_tournament({}, {"id": 1})]

    return ids
