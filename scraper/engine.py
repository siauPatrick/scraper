import json
import sys
import typing
from collections import deque

import requests


SIGN_STDOUT = '-'
FORMAT_CSV = 'csv'
FORMAT_JL = 'jl'


def start(start_url: str, callback: typing.Callable, out_path: str, out_format: str):
    start_task = (start_url, callback)
    tasks = deque([start_task])

    out_file = sys.stdout if out_path == SIGN_STDOUT else open(out_path, 'w', buffering=1)
    if out_format == FORMAT_CSV:
        raise NotImplementedError('this is home work')

    try:
        while tasks:
            url, callback = tasks.popleft()
            print(url)
            resp = requests.get(url)

            for result in callback(resp):
                if isinstance(result, dict):
                    _write_jl(result, out_file)
                else:
                    tasks.append(result)
    finally:
        out_file.close()


def _write_jl(row, out_file):
    json.dump(row, out_file)
    out_file.write('\n')
