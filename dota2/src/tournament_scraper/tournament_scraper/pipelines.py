# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

from .item_validator import ItemValidator
from .items import MatchScraperItem, TournamentScraperItem


class PrintItemPipeline(object):
	def process_item(self, item, spider):
		print(item)
		return item


class CountItemPipeline(object):
	def process_item(self, item, spider):
		if isinstance(item, MatchScraperItem):
			self.counts["match"] += 1
		elif isinstance(item, TournamentScraperItem):
			self.counts["tournament"] += 1
		return item

	def open_spider(self, spider):
		self.counts = { "match": 0, "tournament": 0 }

	def close_spider(self, spider):
		print(self.counts)


class ItemValidatorPipeline(object):
	def process_item(self, item, spider):
		if not self.item_validator.is_valid(item):
			raise DropItem(item)

		return item

	def open_spider(self, spider):
		self.item_validator = ItemValidator()


class TournamentScraperPipeline(object):
	def process_item(self, item, spider):
		return item
