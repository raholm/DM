from enum import Enum

import scrapy

from ..parser import TournamentParser, MatchParser
from ..items import TournamentScraperItem, MatchScraperItem

class ResponseStatus(Enum):
	OK = 200
	ERROR = 404


class TournamentSpider(scrapy.Spider):
	name = "tournament"
	base_url = "https://www.dotabuff.com"

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.tournament_parser = TournamentParser()
		self.match_parser = MatchParser()

	def start_requests(self):
		num_of_leagues = 5
		leagues = range(0, num_of_leagues)
		leagues = [4664]

		for league in leagues:
			url = self.base_url + "/esports/leagues/" + str(league) + "/matches"
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if response.status != ResponseStatus.OK:
			pass

		yield self.parse_tournament(response)

		for match in self.parse_matches(response):
			yield match

		if self.has_more_matches(response):
			next_url = self.next_page_url(response)
			if next_url != "":
				yield scrapy.Request(url=next_url, callback=self.parse_matches)

	def parse_tournament(self, response):
		self.tournament_parser.parse(response)
		return self.create_tournament_item(self.tournament_parser.record)

	def parse_matches(self, response):
		self.match_parser.parse(response)
		return self.create_match_items(self.match_parser.record)

	def has_more_matches(self, response):
		return self.next_page(response) != None

	def next_page(self, response):
		try:
			page_bar = response.xpath("//nav[@class='pagination']")
			page = [page for page in page_bar.xpath(".//span/a[@rel='next']")][0]
		except Exception:
			page = None

		return page

	def next_page_url(self, response):
		try:
			url = self.base_url + self.next_page(response).xpath("@href").extract()[0]
		except:
			url = ""

		return url

	def create_tournament_item(self, record):
		item = TournamentScraperItem()
		item["id"] = record["id"]
		item["name"] = record["name"]
		return item

	def create_match_items(self, record):
		items = []

		for match_id in record["match_ids"]:
			item = MatchScraperItem()
			item["id"] = match_id
			item["tournament_id"] = record["tournament_id"]
			items.append(item)

		return items

