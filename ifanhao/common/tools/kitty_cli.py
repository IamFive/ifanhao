# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-8-24
#
import requests
from BeautifulSoup import BeautifulSOAP

base = 'http://www.btkitty.com/'



def search(keyword, page, type_='all',):
    url = base + 'search.php'

    formdata = dict(submit='%E6%90%9C+%E7%B4%A2',
                    keyword=keyword,
                    type=type_)
    html = requests.post(url, data=formdata)
    BeautifulSOAP(html)


