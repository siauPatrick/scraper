from sys import stdout

import requests


def execute(args):
    resp = requests.get(args.url)
    resp.raise_for_status()

    stdout.write(resp.text)
    stdout.flush()
