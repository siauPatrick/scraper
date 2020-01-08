import csv
import json
import sys
from collections import deque

import requests


FORMAT_CSV = 'csv'
FORMAT_JL = 'jl'
SIGN_STDOUT = '-'


def execute(start_url, callback, out_path, out_format):
    urls = deque([(start_url, callback)])

    out_file = sys.stdout if out_path == SIGN_STDOUT else open(out_path, 'w', buffering=1)
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
                    urls.append(result)
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

    if out_format == FORMAT_CSV:
        return _write_csv
    elif out_format == FORMAT_JL:
        return _write_jl
