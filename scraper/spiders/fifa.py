import requests
from parsel import Selector


BASE_URL = 'https://www.fifaindex.com'
START_URL = BASE_URL + '/players/fifa18wc/'


def parse(resp: requests.Response):
    sel = Selector(resp.text)

    player_css = 'td[data-title="Name"] a::attr(href)'
    tasks = [(BASE_URL + url, parse_player) for url in sel.css(player_css).getall()]

    next_xpath = '//a[text()="Next Page"]/@href'
    next_page = sel.xpath(next_xpath).get()
    if next_page:
        tasks.append((BASE_URL + next_page, parse))

    return tasks


def parse_player(resp: requests.Response):
    sel = Selector(resp.text)
    card = sel.css('.row .pt-3 .card')

    player = {'name': card.css('h5::text').get()}

    metrics = ['Height', 'Weight', 'Age']
    for name in metrics:
        metric_xpath = f'//p[text()="{name} "]/span//text()'
        val_str = card.xpath(metric_xpath).get().split()[0]
        player[name.lower()] = int(val_str)

    return [player]
