import csv
import json
import sys
import typing
from collections import deque

import requests


def execute(start_url, callback, out_path, out_format):
    urls = deque([(start_url, callback)])

    out_file = sys.stdout if out_path == '-' else open(out_path, 'w', buffering=1)
    out_writer = _writer(out_file, out_format)

    try:
        while urls:
            url, callback = urls.popleft()
            resp = requests.get(url)
            resp.raise_for_status()

            for result in callback(resp):
                if isinstance(result, dict):
                    out_writer(result)
                elif isinstance(result, tuple) and len(result) == 2:
                    urls.appendleft(result)
    finally:
        out_file.close()


def _writer(out_file, out_format):
    def _write_jl(row):
        json.dump(row, out_file)
        out_file.write('\n')

    csv_writer = None

    def _write_csv(row):
        nonlocal csv_writer
        if csv_writer is None:
            csv_writer = csv.DictWriter(out_file, row.keys())
            csv_writer.writeheader()

        csv_writer.writerow(row)

    if out_format == 'csv':
        return _write_csv
    elif out_format == 'jl':
        return _write_jl
