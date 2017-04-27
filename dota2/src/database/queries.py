from src.database.client import Dota2DBClient


def get_tournament_ids():
    with Dota2DBClient() as client:
        ids = [tournament["id"]
               for tournament in client.find_tournament({}, {"id": 1})]

    return ids


def get_match_ids():
    with Dota2DBClient() as client:
        ids = [match_id
               for tournament in client.find_tournament({}, {"matches": 1})
               for match_id in tournament["matches"]]

    return ids
