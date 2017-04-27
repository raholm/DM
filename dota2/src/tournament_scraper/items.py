# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TournamentScraperItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()

    def is_valid(self):
        return self._is_valid_id() and self._is_valid_name()

    def _is_valid_id(self):
        return self["id"] >= 0

    def _is_valid_name(self):
        return self["name"] != ""


class MatchScraperItem(scrapy.Item):
    id = scrapy.Field()
    tournament_id = scrapy.Field()

    def is_valid(self):
        return self._is_valid_id() and self._is_valid_tournament_id()

    def _is_valid_id(self):
        return self["id"] >= 0

    def _is_valid_tournament_id(self):
        return self["tournament_id"] >= 0
