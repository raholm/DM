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
    download_delay = 1.5
    max_concurrent_requests = 1

    allowed_domains = ['dotabuff.com']

    custom_settings = {
        'ITEM_PIPELINES': {
            # 'tournament_scraper.pipelines.PrintItemPipeline': 100,
            'src.tournament_scraper.pipelines.ItemValidatorPipeline': 100,
            'src.tournament_scraper.pipelines.CountItemPipeline': 200,
            'src.tournament_scraper.pipelines.MongoDBPipeline': 800,
        }
    }

    def __init__(self, leagues=None, **kwargs):
        super().__init__(**kwargs)

        self.leagues = leagues
        self.tournament_parser = TournamentParser()
        self.match_parser = MatchParser()

    def start_requests(self):
        if self.leagues is not None:
            for league in self.leagues:
                url = self.base_url + "/esports/leagues/" + str(league) + "/matches"
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if not self.is_ok(response):
            return

        for tournament in self.parse_tournament(response):
            yield tournament

        for match in self.parse_matches(response):
            yield match

    def parse_tournament(self, response):
        if not self.is_ok(response):
            return

        self.tournament_parser.parse(response)
        yield self.create_tournament_item(self.tournament_parser.record)

    def parse_matches(self, response):
        if not self.is_ok(response):
            return

        self.match_parser.parse(response)
        for match in self.create_match_items(self.match_parser.record):
            yield match

        if self.has_more_matches(response):
            next_url = self.next_page_url(response)
            if next_url != "":
                yield scrapy.Request(url=next_url, callback=self.parse_matches)

    def has_more_matches(self, response):
        return self.next_page(response) is not None

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
        except Exception:
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

    def is_ok(self, response):
        return response.status != ResponseStatus.OK
