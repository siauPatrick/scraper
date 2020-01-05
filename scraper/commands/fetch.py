from sys import stdout

import requests

from scraper.exceptions import UsageError


def execute(args):
    if args.url:
        resp = requests.get(args.url)
        resp.raise_for_status()

        stdout.write(resp.text)
        stdout.flush()
    else:
        raise UsageError()
