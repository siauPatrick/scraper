from scraper import engine
from scraper.spiders import fifa


def execute(args):
    engine.start(fifa.START_URL, fifa.parse, args.outfile, args.format)
