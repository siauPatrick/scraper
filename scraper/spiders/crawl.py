from collections import deque

import requests
import lxml.html


def execute(start_url):
    urls = deque([(start_url, _parse)])
    items = []

    while urls:
        url, callback = urls.popleft()
        print(url)
        resp = requests.get(url)
        resp.raise_for_status()

        for output in callback(resp):
            if isinstance(output, dict):
                items.append(output)
            elif isinstance(output, tuple) and len(output) == 2:
                urls.appendleft(output)

        print(len(urls))


def _parse(response: requests.Response):
    """
    doc.cssselect('a[href].fi-team-card')
    """
    doc = lxml.html.fromstring(response.text)
    doc.make_links_absolute('https://www.fifa.com')
    team_urls = doc.xpath('//a[contains(@class, "fi-team-card")]/@href')

    return [(url, _parse_team) for url in team_urls[:2]]


def _parse_team(response: requests.Response):
    """
    doc.cssselect('.fi-p__n>a')
    """
    doc = lxml.html.fromstring(response.text)
    doc.make_links_absolute('https://www.fifa.com')
    player_urls = doc.xpath('//div[@class="fi-p__n"]/a/@href')

    return [(url, _parse_player) for url in player_urls]


def _parse_player(response: requests.Response):
    return []
