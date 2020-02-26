from parsel import Selector

from scraper.html import text


def execute(name):
    print(f'Hello {name}')
    html_title = Selector(text).xpath('//title/text()').get()
    print(f'This is title of your html: {html_title}')
