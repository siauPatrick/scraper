import typing
from collections import deque

import requests


def start(start_url: str, callback: typing.Callable):
    start_task = (start_url, callback)
    tasks = deque([start_task])

    while tasks:
        url, callback = tasks.popleft()
        print(url)
        resp = requests.get(url)

        for task in callback(resp):
            tasks.append(task)
