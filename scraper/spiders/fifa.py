from datetime import datetime

import lxml.html
import requests

from scraper.spiders import crawl


START_URL = 'https://www.fifa.com/worldcup/players/_libraries/byposition/all/_players-list'
PLAYER_URL_TPL = 'https://www.fifa.com/worldcup/_libraries/players/player/{player_id}/_player-profile-data'


def execute(out_path, out_format):
    crawl.execute(START_URL, parse, out_path, out_format)


def parse(response: requests.Response):
    """
    doc.cssselect('a[href].fi-p--link')
    """
    doc = lxml.html.fromstring(response.text)
    player_urls = doc.xpath('//a[@data-player-id]/@href')
    player_ids = [url.split('/')[-2] for url in player_urls]

    return [(PLAYER_URL_TPL.format(player_id=player_id), _parse_player) for player_id in player_ids]


def _parse_player(response: requests.Response):
    doc = lxml.html.fromstring(response.text)
    item = dict.fromkeys(['name', 'jersey_number', 'country', 'role', 'age', 'height_cm',
                          'international_caps', 'international_goals', 'date_of_birth'])

    name_items = doc.xpath('//div[@class="fi-p__name"]/text()')
    assert len(name_items) == 1, f'len(name_items): {len(name_items)}'
    item['name'] = name_items[0].strip().title()

    jersey_number_items = doc.xpath('//span[@class="fi-p__num"]/text()')
    assert len(jersey_number_items) == 1, f'len(jersey_number_items): {len(jersey_number_items)}'
    item['jersey_number'] = int(jersey_number_items[0].strip())

    country_items = doc.xpath('//div[@class="fi-p__country"]/text()')
    assert len(country_items) == 1, f'len(country_items): {len(country_items)}'
    item['country'] = country_items[0].strip()

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
