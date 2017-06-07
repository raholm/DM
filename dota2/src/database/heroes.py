from src.database.client import Dota2DBClient
from src.database.queries import get_heroes_dict


class Heroes(object):
    def __init__(self):
        self.__heroes = None
        self.__inverse = None

    @property
    def heroes(self):
        if self.__heroes is None:
            with Dota2DBClient() as client:
                self.__heroes = get_heroes_dict(client)

        return self.__heroes

    @property
    def inverse(self):
        if self.__inverse is None:
            self.__inverse = {v: k for k, v in self.heroes.items()}

        return self.__inverse