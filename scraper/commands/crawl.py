from scraper import engine
from scraper.spiders import fifa


START_URL = 'https://www.fifaindex.com/players/fifa18wc/'


def execute():
    engine.start(START_URL, fifa.parse)
