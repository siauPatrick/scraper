import argparse

from scraper.commands import fetch


def execute():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_fetch = subparsers.add_parser('fetch', usage='scraper fetch <url>')
    parser_fetch.add_argument('url', type=str, help='url for fetching')
    parser_fetch.set_defaults(func=fetch.fetch)

    args = parser.parse_args()
    args.func(args)
