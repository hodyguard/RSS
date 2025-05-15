# SH공사 주택임대 공고 RSS 자동 생성기

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

BASE_URL = "https://www.i-sh.co.kr"
LIST_URL = "https://www.i-sh.co.kr/main/lay2/program/S1T294C297/www/brd/m_247/list.do"


def fetch_items():
    res = requests.get(LIST_URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    items = []

    for li in soup.select("li.b-list__item"):
        title_tag = li.select_one("div.b-list__text > a")
        date_tag = li.select_one("div.b-list__date")
        if not (title_tag and date_tag):
            continue

        title = title_tag.get_text(strip=True)
        link = urljoin(BASE_URL, title_tag['href'])
        pub_date = datetime.strptime(date_tag.get_text(strip=True), "%Y-%m-%d")\
            .strftime('%a, %d %b %Y 00:00:00 +0900')

        items.append((title, link, pub_date))
    return items


def build_rss(items):
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')

    ET.SubElement(channel, 'title').text = 'SH공사 주택임대 공고'
    ET.SubElement(channel, 'link').text = LIST_URL
    ET.SubElement(channel, 'description').text = '서울주택도시공사 주택임대 관련 공고 목록 자동 RSS'
    ET.SubElement(channel, 'language').text = 'ko'

    for title, link, pub_date in items:
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = title
        ET.SubElement(item, 'link').text = link
        ET.SubElement(item, 'pubDate').text = pub_date
        ET.SubElement(item, 'guid').text = link

    tree = ET.ElementTree(rss)
    tree.write("rss.xml", encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    news_items = fetch_items()
    build_rss(news_items)
    print("rss.xml 파일 생성 완료")
