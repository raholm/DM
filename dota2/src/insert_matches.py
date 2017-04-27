import json

import dota2api

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
    max_docs = 1000

    with Dota2DBClient() as client:
        for match_id in get_tournament_match_ids():
            if match_id not in set(get_match_ids()):
                match_data = api.get_match_details(match_id=match_id)
                docs.append(json.loads(match_data.json))

                if len(docs) >= max_docs:
                    client.insert_match(docs)
                    docs.clear()


if __name__ == "__main__":
    main()