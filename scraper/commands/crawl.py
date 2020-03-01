from scraper import crawler


START_URL = 'https://www.fifaindex.com/players/fifa18wc/'


def execute():
    crawler.take_up(START_URL, print)
