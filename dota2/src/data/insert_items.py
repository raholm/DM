import dota2api

from src.database.client import Dota2DBClient


def main():
    api = dota2api.Initialise()

    with Dota2DBClient() as client:
        items = api.get_game_items()

        for item in items["items"]:
            del item["url_image"]
            client.insert("item", item)


if __name__ == '__main__':
    main()
