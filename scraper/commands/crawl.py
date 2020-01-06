from scraper.spiders import crawl


START_URL = 'https://www.fifa.com/worldcup/teams/'


def execute(args):
    crawl.execute(START_URL)
