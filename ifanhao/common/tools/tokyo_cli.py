# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-9-10
#

import requests
from bs4 import BeautifulSoup
from ifanhao.common.tools.utils import build_url
import traceback
from ifanhao.common.tools.strlib import after

base = 'http://tokyotosho.se/search.php?terms={0}&type=15&size_min=&size_max=&username='


def get_search_url(code):
    keywords = code.split('-')
    url = 'http://tokyotosho.se/search.php'
    params = dict(terms=' '.join(keywords), type=15, size_min='',
                  size_max='', username='')
    return build_url(url, params)


def search(code, page=1, type_='all',):
    try:
        html = requests.get(get_search_url(code)).content
        doc = BeautifulSoup(html)
        trs = doc.select('table.listing tr[class]')

        results = []
        for t, b in zip(trs[::2], trs[1::2]):
            magnet = t.select('td.desc-top a:nth-of-type(1)')[0]['href']
            name = t.select('td.desc-top a:nth-of-type(2)')[0].get_text()
            name = name.replace(',. ', '.')

            descs = b.select('td.desc-bot')[0].get_text().split('|')
            size = after(descs[1], ':').strip()
            date = after(descs[2], ':').strip()

            seeders = b.select('td.stats span')[0].get_text()
            leechers = b.select('td.stats span')[1].get_text()
            completed = b.select('td.stats span')[2].get_text()

            record = dict(magnet=magnet, name=name, size=size, date=date,
                          seeders=seeders, leechers=leechers,
                          completed=completed)
            results.append(record)

        return results

    except Exception, e:
        print traceback.format_exc()
        raise e

