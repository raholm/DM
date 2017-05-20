from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from src.database.client import Dota2DBClient
from src.database.queries import get_existing_league_ids
from src.tournament_scraper.spiders.tournament_spider import TournamentSpider


def main():
    with Dota2DBClient() as client:
        existing_league_ids = set(get_existing_league_ids(client))

    start_idx = 0
    num_of_leagues = 5000

    leagues_to_fetch = [i for i in range(start_idx, start_idx + num_of_leagues)
                        if i not in existing_league_ids]

    print(leagues_to_fetch)
    run_spider(**{"leagues": leagues_to_fetch})


def run_spider(**kwargs):
    configure_logging({"LOG_LEVEL": "ERROR"})
    runner = CrawlerRunner()
    d = runner.crawl(TournamentSpider, **kwargs)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished


if __name__ == "__main__":
    main()
