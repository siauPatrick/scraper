import argparse

from scraper.commands import crawl


def parse():
    parser = argparse.ArgumentParser(prog='scraper')
    subparsers = parser.add_subparsers()

    parser_crawl = subparsers.add_parser('crawl')
    parser_crawl.set_defaults(func=crawl.execute)

    args = parser.parse_args()
    args.func()
