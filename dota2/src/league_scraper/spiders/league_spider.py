from enum import Enum

import scrapy

from ..parser import LeagueParser, MatchParser
from ..items import LeagueScraperItem, MatchScraperItem


class ResponseStatus(Enum):
    OK = 200
    ERROR = 404


class LeagueSpider(scrapy.Spider):
    name = "league"
    base_url = "https://www.dotabuff.com"
    # download_delay = 3
    # max_concurrent_requests = 1

    allowed_domains = ['dotabuff.com']

    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'ITEM_PIPELINES': {
            # 'league_scraper.pipelines.PrintItemPipeline': 100,
            'src.league_scraper.pipelines.ItemValidatorPipeline': 100,
            'src.league_scraper.pipelines.CountItemPipeline': 200,
            'src.league_scraper.pipelines.MongoDBPipeline': 800,
            # 'src.league_scraper.pipelines.AddMatchCountForLeaguesPipeline': 900,
        }
    }

    def __init__(self, leagues=None, **kwargs):
        super().__init__(**kwargs)

        self.leagues = leagues
        self.league_parser = LeagueParser()
        self.match_parser = MatchParser()

    def start_requests(self):
        if self.leagues is not None:
            for league in self.leagues:
                url = self.base_url + "/esports/leagues/" + str(league) + "/matches"
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if not self.is_ok(response):
            return

        for league in self.parse_league(response):
            yield league

        for match in self.parse_matches(response):
            yield match

    def parse_league(self, response):
        if not self.is_ok(response):
            return

        self.league_parser.parse(response)
        yield self.create_league_item(self.league_parser.record)

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

    def create_league_item(self, record):
        item = LeagueScraperItem()
        item["id"] = record["id"]
        item["name"] = record["name"]
        item["match_count"] = record["match_count"]
        return item

    def create_match_items(self, record):
        items = []

        for match_id in record["match_ids"]:
            item = MatchScraperItem()
            item["id"] = match_id
            item["league_id"] = record["league_id"]
            items.append(item)

        return items

    def is_ok(self, response):
        return response.status != ResponseStatus.OK
