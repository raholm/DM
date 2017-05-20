# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

from src.database.client import Dota2DBClient
from .items import MatchScraperItem, TournamentScraperItem


class PrintItemPipeline(object):
    def process_item(self, item, spider):
        print(item)
        return item


class CountItemPipeline(object):
    def open_spider(self, spider):
        self.counts = {"match": 0, "tournament": 0}

    def process_item(self, item, spider):
        if isinstance(item, MatchScraperItem):
            self.counts["match"] += 1
        elif isinstance(item, TournamentScraperItem):
            self.counts["tournament"] += 1

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
        self.items = {}

    def process_item(self, item, spider):
        if isinstance(item, TournamentScraperItem):
            self.add_tournament(item)
        elif isinstance(item, MatchScraperItem):
            self.add_match(item)

        return item

    def close_spider(self, spider):
        with Dota2DBClient() as client:
            for _, value in self.items.items():
                if not client.insert("league", value):
                    spider.logger.error("Duplicate key error in league collection: %s" % (value,))

    def add_match(self, item):
        self.items[item["tournament_id"]]["matches"].append(item["id"])

    def add_tournament(self, item):
        self.items[item["id"]] = self.create_tournament(item)

    def create_tournament(self, item):
        return {"id": item["id"], "name": item["name"], "matches": []}
