import argparse

from scraper.commands import fetch, crawl
from scraper.crawler import SIGN_STDOUT, FORMAT_CSV, FORMAT_JL


def execute():
    parser = argparse.ArgumentParser(prog='scraper')
    subparsers = parser.add_subparsers()

    parser_fetch = subparsers.add_parser('fetch')
    parser_fetch.add_argument('url', type=str, help='url for fetching')
    parser_fetch.set_defaults(func=fetch.execute)

    parser_crawl = subparsers.add_parser('crawl')
    parser_crawl.add_argument('-o', '--outfile', metavar='FILE', default=SIGN_STDOUT,
                              help='dump scraped items into FILE (use - for stdout)')
    parser_crawl.add_argument('-f', '--format', default='csv', choices=[FORMAT_CSV, FORMAT_JL],
                              help='format to use for dumping items with -o')
    parser_crawl.set_defaults(func=crawl.execute)

    args = parser.parse_args()
    args.func(args)
