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
import shutil

url = 'http://cn.fanhao.org/people/{0}/'

def default_if_none(v):
    if v == '未填写':
        return ''
    return v


def get_actor(index):

    try:
        response = requests.get(url.format(index), timeout=8)
        if response.status_code != 200:
            return None

        doc = BeautifulSoup(response.content)


        if doc.select('#error_msg'):
            return None

        name_txt = doc.select('#people_detail h2')[0].get_text().split('|')
        if len(name_txt) == 2:
            cn_name = name_txt[0].strip()
            name = name_txt[1]
        else:
            cn_name = name = name_txt[0]

        details = [td.get_text()
                   for td in doc.select('.detail_table td')[1::2]]

        avatar = len(doc.select('.people_logo_wrap a'))

        if avatar:
            a_url = 'http://fanhao.org/upload/people_logo/{}/{}.jpg'.format(index % 1000, index)
            response = requests.get(a_url, stream=True)
            with open('avatars/{}.jpg'.format(index), 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response


        birth = default_if_none(details[0]).replace('.', '-')
        height = default_if_none(details[3])
        weight = default_if_none(details[4])
        cup = default_if_none(details[5])
        chest = default_if_none(details[6])
        waist = default_if_none(details[7])
        hip = default_if_none(details[8])
        result = (name, cn_name, birth, height, weight, cup, chest, waist, hip, index, avatar)
        result = [str(item).replace(' cm', '').strip() for item in result]
        print 'success: ' + str(index)
        return result
    except Exception, e:
        print 'failed: ' + str(index)
        print traceback.format_exc()

    return None

def start():
    pool = ThreadPool(80)


    for i in range(0, (24915 - 10000) / 1000 + 1):
        s = 10000 + 1000 * i
        e = min(24915, 10000 + 1000 * (i + 1) - 1)
        print 'now: {0}-{1}'.format(s, e)
        result = pool.map(get_actor, range(s, e))
        with open('a{0}.txt'.format(i), 'w') as f:
            for record in result:
                if record:
                    f.write(','.join(record) + '\n')
            f.flush()

#    result = pool.map(get_actor, range(10000, 15000))
#    with open('actors1.txt', 'w') as f:
#        for record in result:
#            if record:
#                f.write(','.join(record) + '\n')
#        f.flush()
#
#    result = pool.map(get_actor, range(15001, 20000))
#    with open('actors2.txt', 'w') as f:
#        for record in result:
#            if record:
#                f.write(','.join(record) + '\n')
#        f.flush()
#
#    result = pool.map(get_actor, range(20001, 24915))
#    with open('actors3.txt', 'w') as f:
#        for record in result:
#            if record:
#                f.write(','.join(record) + '\n')
#        f.flush()

start()

# print ','.join(get_actor(10020))
# print get_actor(10386)
