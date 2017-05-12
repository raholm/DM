import dota2api

from src.database.client import Dota2DBClient


def main():
    api = dota2api.Initialise()

    with Dota2DBClient() as client:
        heroes = api.get_heroes()

        for hero in heroes["heroes"]:
            del hero["url_large_portrait"]
            del hero["url_small_portrait"]
            del hero["url_full_portrait"]
            del hero["url_vertical_portrait"]
            client.insert(hero, "hero")


if __name__ == '__main__':
    main()
