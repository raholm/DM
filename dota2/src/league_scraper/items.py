# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LeagueScraperItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    match_count = scrapy.Field()

    def is_valid(self):
        return self._is_valid_id() and self._is_valid_name() and self._is_valid_match_count()

    def _is_valid_id(self):
        return self["id"] >= 0

    def _is_valid_name(self):
        return self["name"] != ""

    def _is_valid_match_count(self):
        return self["match_count"] > 0


class MatchScraperItem(scrapy.Item):
    id = scrapy.Field()
    league_id = scrapy.Field()

    def is_valid(self):
        return self._is_valid_id() and self._is_valid_league_id()

    def _is_valid_id(self):
        return self["id"] >= 0

    def _is_valid_league_id(self):
        return self["league_id"] >= 0
