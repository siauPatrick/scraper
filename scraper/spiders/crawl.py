import json
import typing
from collections import deque

import requests


def execute(start_url, callback, outfile: typing.TextIO):
    urls = deque([(start_url, callback)])

    while urls:
        url, callback = urls.popleft()
        resp = requests.get(url)
        resp.raise_for_status()

        for result in callback(resp):
            if isinstance(result, dict):
                json.dump(result, outfile)
                outfile.write('\n')
            elif isinstance(result, tuple) and len(result) == 2:
                urls.appendleft(result)
