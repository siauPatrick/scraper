from collections import deque

import requests

from scraper.spiders import fifa


def execute(start_url):
    urls = deque([(start_url, fifa.parse)])
    items = []

    while urls:
        url, callback = urls.popleft()
        print(url)
        resp = requests.get(url)
        resp.raise_for_status()

        for output in callback(resp):
            if isinstance(output, dict):
                print(output)
                items.append(output)
            elif isinstance(output, tuple) and len(output) == 2:
                urls.appendleft(output)
