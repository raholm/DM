class Parser(object):
    def __init__(self):
        self.record = None

    def parse(self, response):
        raise NotImplementedError("Parser.parse")


class TournamentParser(Parser):
    def __init__(self):
        self.base_xpath = "//div[@class='container-inner']"

    def parse(self, response):
        self.record = {}
        self.record["id"] = self.parse_id(response)
        self.record["name"] = self.parse_name(response)
        return self

    def parse_id(self, response):
        try:
            id = int(response.url.split("/")[-2])
        except Exception:
            id = -1

        return id

    def parse_name(self, response):
        xpath = ".//div[@class='header-content-title']/h1/text()"

        try:
            name = response.xpath(self.base_xpath).xpath(xpath).extract()[0]
        except IndexError:
            name = ""

        return name


class MatchParser(Parser):
    def __init__(self):
        self.base_xpath = "//div[@class='content-inner']"

    def parse(self, response):
        self.record = {}
        self.record["match_ids"] = self.parse_match_ids(response)
        self.record["tournament_id"] = self.parse_tournament_id(response)
        return self

    def parse_tournament_id(self, response):
        try:
            id = int(response.url.split("/")[-2])
        except Exception:
            id = -1

        return id

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
