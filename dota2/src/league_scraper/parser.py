class Parser(object):
    def __init__(self):
        self.record = None

    def parse(self, response):
        raise NotImplementedError("Parser.parse")


class LeagueParser(Parser):
    def __init__(self):
        super().__init__()
        self.base_xpath = "//div[contains(@class, 'container-inner')]"

    def parse(self, response):
        self.record = {"id": self.parse_id(response),
                       "name": self.parse_name(response),
                       "match_count": self.parse_match_count(response)}
        return self

    def parse_id(self, response):
        try:
            league_id = int(response.url.split("/")[-2])
        except Exception:
            league_id = -1

        return league_id

    def parse_name(self, response):
        xpath = ".//div[@class='header-content-title']/h1/text()"

        try:
            league_name = response.xpath(self.base_xpath).xpath(xpath).extract()[0]
        except Exception:
            league_name = ""

        return league_name

    def parse_match_count(self, response):
        xpath = ".//div[@class='viewport']/text()"

        try:
            match_count = response.xpath(self.base_xpath).xpath(xpath).extract()[0]
            match_count = int(match_count.strip().split()[-1])
        except Exception:
            match_count = -1

        return match_count


class MatchParser(Parser):
    def __init__(self):
        super().__init__()
        self.base_xpath = "//div[@class='content-inner']"

    def parse(self, response):
        self.record = {"match_ids": self.parse_match_ids(response),
                       "league_id": self.parse_league_id(response)}
        return self

    def parse_league_id(self, response):
        try:
            match_id = int(response.url.split("/")[-2])
        except Exception:
            match_id = -1

        return match_id

    def parse_match_ids(self, response):
        matches_xpath = ".//tbody"
        match_xpath = ".//tr/td/a[contains(@href, '/matches/')]"

        try:
            matches = response.xpath(self.base_xpath).xpath(matches_xpath)
            match_ids = [self.parse_match_id(match)
                         for match in matches.xpath(match_xpath)]
        except Exception:
            match_ids = []

        return match_ids

    def parse_match_id(self, response):
        xpath = "text()"

        try:
            match_id = int(response.xpath(xpath).extract()[0])
        except Exception:
            match_id = -1

        return match_id
