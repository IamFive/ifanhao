# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-8-27
#
from bs4 import BeautifulSoup
import requests
import traceback
import urlparse
import urllib
from multiprocessing.pool import ThreadPool
import time


BASE_URL = 'http://www.javlibrary.com/cn/'
START_URL = BASE_URL + 'genres.php'



def get_text(bs_doc, selector, start=0, end=0, index=0):
    try:
        temp = bs_doc.select(selector)[index].get_text().strip()
        return temp[start: end if end != 0 else len(temp)];
    except Exception, e:
        return '';


def build_url(url, params):
    urlparts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(urlparts[4]))
    query.update(params)
    urlparts[4] = urllib.urlencode(query)
    return urlparse.urlunparse(urlparts)

def after(s, pat):
    # returns the substring after pat in s.
    # if pat is not in s, then return a null string!
    pos = s.find(pat)
    if pos != -1:
        return s[pos + len(pat):]
    return ""


def get_groups():
    html = requests.get(START_URL).content
    document = BeautifulSoup(html)
    groups = document.select('div.genreitem a')
    return [g['href'] for g in groups]
#    return ['vl_genre.php?g=a46q']

def get_group_names():
    html = requests.get(START_URL).content
    document = BeautifulSoup(html)
    groups = document.select('div.genreitem a')
    return [g.get_text() for g in groups]


def get_grouped_av_links(group_url):

    url = BASE_URL + group_url

    page = 0
    goon = True
    result = []
    while goon:
        page += 1
        try:
            print 'scrum page {} for group {}'.format(page, group_url)
            paginate_url = build_url(url, dict(mode=2, page=page))

            html = requests.get(paginate_url).content
            document = BeautifulSoup(html)
            goon = len(document.select('div.page_selector a.next')) > 0
            videos = document.select('div.video')
            links = [after(video.find('a')['href'], './?v=') for video in videos]
            result.extend(links)
        except:
            print traceback.format_exc()

    return result

def get_av_links():
    with open(r'urls.txt', 'a') as f:
        group_urls = get_groups()
#        idx = group_urls.index('vl_genre.php?g=be')
        for group_url in group_urls[0:]:
            links = get_grouped_av_links(group_url)
            f.write('\n'.join(links))
            f.write('\n')
            f.flush()


def get_av(token):
    token = token.strip()
    if len(token) == 0:
        return None

    url = build_url(BASE_URL, dict(v=token.strip()))
    try:
        response = requests.get(url, timeout=8)
        if response.status_code != 200:
            print 'Faild: ' + token + ', status: ' + str(response.status_code)
            time.sleep(60)
            print 'try sleep for 60s'
            return None

        html = response.content
        doc = BeautifulSoup(html)
        title = get_text(doc, 'div#video_title .post-title a')
        code = get_text(doc, 'div#video_id td.text')

        if title.index(code) > -1:
            title = after(title, code).strip()


        published_on = get_text(doc, 'div#video_date td.text')
        director = get_text(doc, 'div#video_director span.director a')
        maker = get_text(doc, 'div#video_maker span.maker a')
        label = get_text(doc, 'div#video_label span.label a')
        tags = '|'.join([tag.get_text() for tag in doc.select('div#video_genres a')])
        actors = '|'.join([actor.get_text() for actor in doc.select('div#video_cast span.star a')])
        result = ','.join(['"' + t.encode('utf-8') + '"' for
                t in (title, code, published_on, director, maker, label, tags, actors)])
        print 'Success: ' + token
        return result
    except:
        print 'Faild: ' + token
        return None

def get_avs():
    with open(r'tokens.txt', 'r')  as f:
        lines = f.readlines()

    with open('a.txt', 'a') as f2:
        for line in lines:
            result = get_av(line)
            if result:
                f2.write(result)
                f2.write('\n')

        f2.write('\n')
        f2.flush()

get_avs()
# get_av_links()
# print '\n'.join(get_av('javlial4si'))
