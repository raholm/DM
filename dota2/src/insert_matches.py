import json

import dota2api
from dota2api.src.exceptions import APIError

from src.database.client import Dota2DBClient
from src.database.queries import get_tournament_match_ids, get_match_ids


def test():
    api = dota2api.Initialise()
    match = api.get_match_details(match_id=2836936292)
    parsed = json.loads(match.json)
    print(json.dumps(parsed, indent=4, sort_keys=True))


def main():
    api = dota2api.Initialise()
    docs = []
    max_docs = 1

    match_ids_to_fetch = get_tournament_match_ids()
    match_ids_fetched = set(get_match_ids())
    counter = 1

    with Dota2DBClient() as client:
        for match_id in match_ids_to_fetch:
            if match_id not in match_ids_fetched:
                try:
                    match_data = api.get_match_details(match_id=match_id, raw_mode=True)
                except APIError as e:
                    print(e)
                    print(match_id)
                    continue

                try:
                    json_item = json.loads(match_data.json)

                    # if "dire_logo" in json_item:
                    #     del json_item["dire_logo"]
                    #
                    # if "radiant_logo" in json_item:
                    #     del json_item["radiant_logo"]

                    docs.append(json_item)
                except Exception as e:
                    print(e)
                    print(match_id)
                    continue

                if len(docs) >= max_docs:
                    print(counter)
                    client.insert_match(docs)
                    docs.clear()
                    counter += 1

        if len(docs) > 0:
            client.insert_match(docs)


if __name__ == "__main__":
    main()