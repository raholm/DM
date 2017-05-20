import pandas as pd

from src.util.date import is_within_time


def get_all_league_match_ids(client):
    return [match_id
            for tournament in client.find("league", {}, {"matches": 1})
            for match_id in tournament["matches"]]


def get_existing_match_ids(client):
    return [match["match_id"]
            for match in client.find("match", {}, {"match_id": 1})]


def get_match_picks_bans_df(client, match_id_or_ids):
    if not isinstance(match_id_or_ids, (tuple, list)):
        match_id_or_ids = [match_id_or_ids]

    df = pd.DataFrame()

    with client.find("match",
                     filter={"match_id": {"$in": match_id_or_ids}},
                     projection={"picks_bans": 1}) \
            as matches:
        for match in matches:
            new_df = pd.DataFrame(match["picks_bans"])
            df = df.append(new_df, ignore_index=True)

    return df


def get_match_ids_in_league(client, league):
    with client.find("league",
                     filter={"name": league},
                     projection={"matches": 1}) as leagues:
        for league in leagues:
            for match_id in league["matches"]:
                yield match_id


def get_match_ids_from(client, league, time_interval):
    match_ids = []

    for match_id in get_match_ids_in_league(client, league):
        with client.find("match",
                         filter={"match_id": match_id},
                         projection={"start_time": 1}) as matches:
            for match in matches:
                if is_within_time(match["start_time"], time_interval):
                    match_ids.append(match_id)

    return match_ids


def get_time_frame(client, league):
    times = []

    for match_id in get_match_ids_in_league(client, league):
        with client.find("match",
                         filter={"match_id": match_id},
                         projection={"start_time": 1}) as matches:
            for match in matches:
                times.append(match["start_time"])

    return min(times), max(times)


def get_existing_league_ids(client):
    with client.find("league", {}, {"id": 1}) as leagues:
        return [league["id"]
                for league in leagues]


def get_leagues_to_scrape(client):
    with client.find("league",
                     {"$where": "this.matches.length != this.match_count"},
                     {"id": 1}) as leagues:
        return [league["id"] for league in leagues]


def get_num_matches_in_leagues(client):
    with client.aggregate("league",
                          {"$project": {"id": "$id", "match_count": {"$size": "$matches"}}}) as leagues:
        return {league["id"]: league["match_count"]
                for league in leagues}


def get_league_matches_dict(client):
    with client.find("league", {}, {"id": 1, "matches": 1}) as leagues:
        return {league["id"]: league["matches"]
                for league in leagues}


def get_total_num_league_matches(client):
    with client.aggregate("league", {"$group": {"_id": {}, "count": {"$sum": {"$size": "$matches"}}}}) as counts:
        for count in counts:
            return count["count"]
