from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from src.database.queries import get_tournament_ids
from src.tournament_scraper.spiders.tournament_spider import TournamentSpider


def main():
    fetched_tournament_ids = get_tournament_ids()
    start_idx = 200
    num_of_tournaments = 1000

    tournaments_to_fetch = [i for i in range(start_idx, start_idx + num_of_tournaments)
                            if i not in fetched_tournament_ids]

    run_spider(**{"leagues": tournaments_to_fetch})


def run_spider(**kwargs):
    configure_logging({"LOG_LEVEL": "ERROR"})
    runner = CrawlerRunner()
    d = runner.crawl(TournamentSpider, **kwargs)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished


if __name__ == "__main__":
    main()
