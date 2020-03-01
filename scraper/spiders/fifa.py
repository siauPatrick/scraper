import requests


BASE_URL = 'https://www.fifaindex.com'


def parse(resp: requests.Response):
    index = resp.text.find('Next Page')
    if index == -1:
        return

    url = []
    for ch in resp.text[index - 3::-1]:
        if ch == '"':
            break
        url.append(ch)

    assert url, 'blank url'
    return BASE_URL + ''.join(url[::-1]), parse
