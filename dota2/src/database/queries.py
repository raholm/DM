import pandas as pd

from src.util.date import is_within_time
from src.database.client import Dota2DBClient


def get_tournament_ids():
    with Dota2DBClient() as client:
        ids = [tournament["id"]
               for tournament in client.find_tournament({}, {"id": 1})]

    return ids


def get_tournament_match_ids():
    with Dota2DBClient() as client:
        ids = [match_id
               for tournament in client.find_tournament({}, {"matches": 1})
               for match_id in tournament["matches"]]

    return ids


def get_match_ids():
    with Dota2DBClient() as client:
        ids = [match["match_id"]
               for match in client.find_match({}, {"match_id": 1})]

    return ids


def get_picks_bans(client, match_id_or_ids):
    if not isinstance(match_id_or_ids, (tuple, list)):
        match_id_or_ids = [match_id_or_ids]

    df = pd.DataFrame()

    with client.find_match(filter={"match_id": {"$in": match_id_or_ids}},
                           projection={"picks_bans": 1}) \
            as documents:
        for document in documents:
            new_df = pd.DataFrame(document["picks_bans"])
            df = df.append(new_df, ignore_index=True)

    return df


def get_tournament_matches(client, tournament):
    with client.find_tournament(filter={"name": tournament},
                                projection={"matches": 1}) as documents:
        for doc in documents:
            for match_id in doc["matches"]:
                yield match_id


def get_match_ids_from(client, tournament, time_interval):
    match_ids = []

    for match_id in get_tournament_matches(client, tournament):
        with client.find_match(filter={"match_id": match_id},
                               projection={"start_time": 1}) as matches:
            for match in matches:
                if is_within_time(match["start_time"], time_interval):
                    match_ids.append(match_id)

    return match_ids


def get_time_frame(client, tournament):
    times = []

    for match_id in get_tournament_matches(client, tournament):
        with client.find_match(filter={"match_id": match_id},
                               projection={"start_time": 1}) as matches:
            for match in matches:
                times.append(match["start_time"])

    return min(times), max(times)
