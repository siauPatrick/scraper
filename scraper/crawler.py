import typing

import requests


def take_up(start_url: str, callback: typing.Callable):
    resp = requests.get(start_url)
    callback(resp.text)
