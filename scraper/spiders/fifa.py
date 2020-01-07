import sys
from datetime import datetime

import lxml.html
import requests

from scraper.spiders import crawl


BASE_URL = 'https://www.fifa.com'
START_URL = BASE_URL + '/worldcup/teams/'


def execute():
    crawl.execute(START_URL, parse, sys.stdout)


def parse(response: requests.Response):
    """
    doc.cssselect('a[href].fi-team-card')
    """
    doc = lxml.html.fromstring(response.text)
    doc.make_links_absolute('https://www.fifa.com')
    team_urls = doc.xpath('//a[contains(@class, "fi-team-card")]/@href')

    return [(url, _parse_team) for url in team_urls]


def _parse_team(response: requests.Response):
    """
    doc.cssselect('.fi-p__n>a')
    """
    doc = lxml.html.fromstring(response.text)
    doc.make_links_absolute('https://www.fifa.com')
    player_urls = doc.xpath('//div[@class="fi-p__n"]/a/@href')

    return [(f'{url}profile/', _parse_player) for url in player_urls]


def _parse_player(response: requests.Response):
    doc = lxml.html.fromstring(response.text)
    item = {}

    name_items = doc.xpath('//div[@class="fi-p__name"]/text()')
    assert len(name_items) == 1, f'len(name_items): {len(name_items)}'
    item['name'] = name_items[0].strip().title()

    country_items = doc.xpath('//div[@class="fi-p__country"]/text()')
    assert len(country_items) == 1, f'len(country_items): {len(country_items)}'
    item['team_country'] = country_items[0].strip()

    role_items = doc.xpath('//div[@class="fi-p__role"]/text()')
    assert len(role_items) == 1, f'len(role_items): {len(country_items)}'
    item['role'] = role_items[0].strip().lower()

    numbers = doc.xpath('//div[contains(@class, "fi-p__profile-info")]//div[@class="fi-p__profile-number"]')
    for el in numbers:
        text = el.text.strip().lower().replace(' ', '_')
        number_items = el.xpath('div[@class="fi-p__profile-number__number"]/text()')
        assert len(number_items) == 1, f'len(number_items): {len(number_items)}'
        number_str = number_items[0].strip()

        if text == 'height':
            number_str, _ = number_str.split()
            item['height_cm'] = float(number_str)
        else:
            item[text] = int(number_str)

    texts = doc.xpath('//div[contains(@class, "fi-p__profile-info")]//div[contains(@class, "fi-p__profile-text")]')
    for el in texts:
        text = el.text.strip().lower().replace(' ', '_')
        text_items = el.xpath('span/text()')
        assert len(text_items) == 1, f'len(text_items): {len(text_items)}'
        text_val = text_items[0].strip()

        if text == 'date_of_birth':
            text_val = datetime.strptime(text_val, "%d %B %Y").date().isoformat()

        item[text] = text_val

    return [item]
