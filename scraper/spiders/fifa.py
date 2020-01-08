from datetime import datetime

import lxml.html
import requests
from lxml.etree import XPath

from scraper.spiders import crawl


# url constants
START_URL = 'https://www.fifa.com/worldcup/players/_libraries/byposition/all/_players-list'
PLAYER_URL_TPL = 'https://www.fifa.com/worldcup/_libraries/players/player/{player_id}/_player-profile-data'

# data constants
LABEL_HEIGHT = 'height'
LABEL_DATE_OF_BIRTH = 'date_of_birth'
DATE_OF_BIRTH_FORMAT = '%d %B %Y'

# xpath selectors
name_xpath = XPath('//div[@class="fi-p__name"]/text()')
country_xpath = XPath('//div[@class="fi-p__country"]/text()')
role_xpath = XPath('//div[@class="fi-p__role"]/text()')
jersey_number_xpath = XPath('//span[@class="fi-p__num"]/text()')

info_number_xpath = XPath('//div[contains(@class, "fi-p__profile-info")]//div[@class="fi-p__profile-number"]')
number_xpath = XPath('div[@class="fi-p__profile-number__number"]/text()')

info_text_xpath = XPath('//div[contains(@class, "fi-p__profile-info")]//div[contains(@class, "fi-p__profile-text")]')
text_xpath = XPath('span/text()')


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
    item = dict.fromkeys(['name', 'jersey_number', 'country', 'role', 'age', 'height',
                          'international_caps', 'international_goals', 'date_of_birth'])

    item['name'] = _extract_first_val(name_xpath(doc)).title()
    item['country'] = _extract_first_val(country_xpath(doc))
    item['role'] = _extract_first_val(role_xpath(doc)).lower()

    jersey_number = _extract_first_val(jersey_number_xpath(doc))
    item['jersey_number'] = int(jersey_number)

    _fill_numbers(item, doc)
    _fill_texts(item, doc)

    return [item]


def _extract_first_val(items):
    assert len(items) == 1, f'len(items): {len(items)}'
    return items[0].strip()


def _fill_numbers(item, doc):
    for el in info_number_xpath(doc):
        info_number = _extract_first_val(number_xpath(el))
        label = el.text.strip().lower().replace(' ', '_')

        if label == LABEL_HEIGHT:
            info_number, _ = info_number.split()
            item[label] = float(info_number)
        else:
            item[label] = int(info_number)


def _fill_texts(item, doc):
    for el in info_text_xpath(doc):
        info_text = _extract_first_val(text_xpath(el))
        label = el.text.strip().lower().replace(' ', '_')

        if label == LABEL_DATE_OF_BIRTH:
            info_text = datetime.strptime(info_text, DATE_OF_BIRTH_FORMAT).date().isoformat()

        item[label] = info_text
