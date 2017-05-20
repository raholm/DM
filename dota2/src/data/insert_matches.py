import json

import dota2api
from dota2api.src.exceptions import APIError

from src.database.client import Dota2DBClient
from src.database.queries import get_all_league_match_ids, get_existing_match_ids


def main():
    api = dota2api.Initialise()
    docs = []
    max_docs = 100
    counter = 1

    with Dota2DBClient() as client:
        match_ids_to_fetch = get_all_league_match_ids(client)
        existing_match_ids = set(get_existing_match_ids(client))

        for match_id in match_ids_to_fetch:
            if match_id not in existing_match_ids:
                try:
                    match_data = api.get_match_details(match_id=match_id, raw_mode=True)
                except APIError as e:
                    print(e)
                    print(match_id)
                    continue

                try:
                    dict_obj = json.loads(match_data.json)

                    if "dire_logo" in dict_obj:
                        del dict_obj["dire_logo"]

                    if "radiant_logo" in dict_obj:
                        del dict_obj["radiant_logo"]

                    existing_match_ids.add(dict_obj["match_id"])
                    docs.append(dict_obj)
                except Exception as e:
                    print(e)
                    print(match_id)
                    continue

                if len(docs) >= max_docs:
                    print(counter)
                    client.insert("match", docs)
                    docs.clear()
                    counter += 1

        if len(docs) > 0:
            client.insert("match", docs)


if __name__ == "__main__":
    main()
