import typing
from collections import deque

import requests


def start(start_url: str, callback: typing.Callable):
    start_task = (start_url, callback)
    urls = deque([start_task])

    while urls:
        url, callback = urls.popleft()
        print(url)
        resp = requests.get(url)

        next_task = callback(resp)
        if next_task:
            urls.append(next_task)
