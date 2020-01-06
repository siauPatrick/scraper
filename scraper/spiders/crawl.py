from collections import deque

import requests
import lxml.html


def execute(start_url):
    urls = deque([start_url])

    while urls:
        url = urls.popleft()
        resp = requests.get(url)
        resp.raise_for_status()

        doc = lxml.html.fromstring(resp.text)
        doc.make_links_absolute('https://www.fifa.com')
        urls.extend(doc.xpath('//a[contains(@class, "fi-team-card")]/@href'))

        print(urls)

    # doc.xpath('//a[contains(@class, "fi-team-card")]/@href')
    # doc.cssselect('a[href].fi-team-card')
