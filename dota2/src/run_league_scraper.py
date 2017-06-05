import random

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from src.database.client import Dota2DBClient
from src.database.queries import get_leagues_to_scrape
from src.league_scraper.spiders.league_spider import LeagueSpider


def main():
    with Dota2DBClient() as client:
        leagues_to_scrape = get_leagues_to_scrape(client)

    random.shuffle(leagues_to_scrape)
    print(len(leagues_to_scrape))
    print(leagues_to_scrape)
    run_spider(**{"leagues": leagues_to_scrape[:2]})


def run_spider(**kwargs):
    configure_logging({"LOG_LEVEL": "WARNING"})
    runner = CrawlerRunner()
    d = runner.crawl(LeagueSpider, **kwargs)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished


if __name__ == "__main__":
    main()
