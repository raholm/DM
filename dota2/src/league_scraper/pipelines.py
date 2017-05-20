# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

from src.database.client import Dota2DBClient
from src.database.queries import get_league_matches_dict
from .items import MatchScraperItem, LeagueScraperItem


class PrintItemPipeline(object):
    def process_item(self, item, spider):
        print(item)
        return item


class CountItemPipeline(object):
    def open_spider(self, spider):
        self.counts = {"match": 0, "league": 0}

    def process_item(self, item, spider):
        if isinstance(item, MatchScraperItem):
            self.counts["match"] += 1
        elif isinstance(item, LeagueScraperItem):
            self.counts["league"] += 1

        return item

    def close_spider(self, spider):
        print(self.counts)


class ItemValidatorPipeline(object):
    def process_item(self, item, spider):
        if not item.is_valid():
            spider.logger.error("Invalid item found: %s" % (item,))
            raise DropItem(item)

        return item


class MongoDBPipeline(object):
    def open_spider(self, spider):
        self.leagues = {}

        with Dota2DBClient() as client:
            self.existing_leagues = get_league_matches_dict(client)

    def process_item(self, item, spider):
        if isinstance(item, LeagueScraperItem):
            self.add_league(item)
        elif isinstance(item, MatchScraperItem):
            self.add_match(item)

        return item

    def close_spider(self, spider):
        with Dota2DBClient() as client:
            for league in self.leagues.values():
                if self.has_league(league):
                    if not self.has_additional_matches(league):
                        continue

                    merged_matches = self.get_merged_matches(league)
                    if not client.update("league", {"id": league["id"]}, {"$set": {"matches": merged_matches}}):
                        spider.logger.error("Failed to update: %s" % (league,))
                else:
                    if not client.insert("league", league):
                        spider.logger.error("Failed to insert: %s" % (league,))

    def add_match(self, item):
        self.leagues[item["league_id"]]["matches"].append(item["id"])

    def add_league(self, item):
        self.leagues[item["id"]] = self.create_league(item)

    def create_league(self, item):
        return {"id": item["id"], "name": item["name"], "match_count": item["match_count"], "matches": []}

    def has_league(self, league):
        return self.existing_leagues.get(league["id"]) is not None

    def has_additional_matches(self, league):
        existing_matches = self.existing_leagues[league["id"]]

        for match_id in league["matches"]:
            if match_id not in existing_matches:
                return True
        return False

    def get_merged_matches(self, league):
        return list(set(league["matches"] + self.existing_leagues[league["id"]]))


class AddMatchCountForLeaguesPipeline(object):
    def open_spider(self, spider):
        self.leagues = {}

    def process_item(self, item, spider):
        if isinstance(item, LeagueScraperItem):
            self.add_league(item)

        return item

    def close_spider(self, spider):
        with Dota2DBClient() as client:
            for league in self.leagues.values():
                print(league)
                # if not client.update("league", {"id": league["id"]}, {"$set": {"match_count": league["match_count"]}}):
                #     spider.logger.error("Failed to update: %s" % (league,))

    def add_league(self, item):
        self.leagues[item["id"]] = dict(item)
