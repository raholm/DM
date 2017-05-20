import dota2api

from src.database.client import Dota2DBClient
from src.database.queries import get_existing_league_ids


def get_leagues(api_con):
    league_listing = api_con.get_league_listing()

    for leagues in league_listing.items():
        for league in leagues[1]:
            yield {"id": league["leagueid"],
                   "name": league["name"],
                   "matches": get_match_ids_in_league(api_con, league)}


def get_match_ids_in_league(api_con, league):
    match_history = api_con.get_match_history(league_id=league["leagueid"])

    if match_history["status"] == 1:
        return [match["match_id"]
                for match in match_history["matches"]]

    raise ValueError("Could not find match history for %s" % (league["leagueid"],))


def main():
    docs = []
    api = dota2api.Initialise()
    max_docs = 100

    with Dota2DBClient() as client:
        league_ids = set(get_existing_league_ids(client))
        try:
            for league in get_leagues(api):
                if league["id"] in league_ids:
                    continue

                league_ids.add(league["id"])
                docs.append(league)

                if len(docs) >= max_docs:
                    client.insert("league", docs)
                    docs.clear()
        except ValueError as e:
            print(e)
            return

    if len(docs) > 0:
        client.insert("league", docs)


if __name__ == '__main__':
    main()
