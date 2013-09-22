# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-9-12
#
import requests
import traceback
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
from ifanhao.common.tools.strlib import before

url = 'http://cn.fanhao.org/people/{0}/'

def default_if_none(v):
    if v == '未填写':
        return ''
    return v


def get_actor(index):

    index = str(index)

    try:
        html = requests.get(url.format(index), timeout=8).content
        doc = BeautifulSoup(html)

        name_txt = doc.select('#people_detail h2')[0].get_text().split('|')
        if len(name_txt) == 2:
            cn_name = name_txt[0].strip()
            name = before(name_txt[1], '(').strip()
        else:
            cn_name = name = name_txt[0]

        details = [td.get_text()
                   for td in doc.select('.detail_table td')[1::2]]

        birth = default_if_none(details[0]).replace('.', '-')
        height = default_if_none(details[3])
        weight = default_if_none(details[4])
        cup = default_if_none(details[5])
        chest = default_if_none(details[6])
        waist = default_if_none(details[7])
        hip = default_if_none(details[8])

        result = (name, cn_name, birth, height, weight, cup, chest, waist, hip, index)
        result = [item.replace(' cm', '') for item in result]
        print 'success: ' + str(index)
        return result
    except Exception, e:
        print 'failed: ' + str(index)

    return None

def start():
    pool = ThreadPool(80)
#    result = pool.map(get_actor, range(10000, 15000))
# #    result = pool.map(get_actor, range(10000, 10002))
#    with open('actors1.txt', 'w') as f:
#        for record in result:
#            if record:
#                f.write(','.join(record) + '\n')
#        f.flush()

    result = pool.map(get_actor, range(15001, 20000))
    with open('actors2.txt', 'w') as f:
        for record in result:
            if record:
                f.write(','.join(record) + '\n')
        f.flush()

    result = pool.map(get_actor, range(20001, 24915))
    with open('actors3.txt', 'w') as f:
        for record in result:
            if record:
                f.write(','.join(record) + '\n')
        f.flush()

start()
