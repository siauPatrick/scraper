import argparse

from scraper.commands import greeting


def parse():
    parser = argparse.ArgumentParser(prog='scraper')
    parser.add_argument('-g', '--greeting', metavar='NAME', default="world", help='greet NAME', dest='name')

    args = parser.parse_args()
    greeting.execute(args.name)
