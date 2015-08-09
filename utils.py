# coding: utf-8

import requests
from pyquery import PyQuery as pq
from config import USER_AGENTS, logger
import random
import datetime
import json
from itertools import chain, count
import os
from multiprocessing import Pool


def get_content(url):
    r = requests.get(url, headers={'User-Agent': random.choice(USER_AGENTS)})
    assert r.status_code == 200
    if r.encoding in ('ISO-8859-1', 'gb2312'):
        logger.debug(
            'Turn coding from {coding} to gbk'.format(coding=r.encoding))
        r.encoding = 'gbk'
    return r.text


def bitauto_trace(model, deadline):
    URL_FORMAT = 'http://baa.bitauto.com/{model}/index-all-all-{page}-1.html'

    for page in count(1):
        url = URL_FORMAT.format(page=page, model=model)
        logger.debug('bitauto trace {url}'.format(url=url))
        content = get_content(url)
        d = pq(content)
        rows = d('div.postslist_fist_title').nextAll('div.postslist_xh')

        for row in rows:
            i = pq(row)
            title = i('li.bt span').text().strip()
            href = i('li.bt a').attr('href')
            author = i('li.zz a').html().strip()

            now = datetime.datetime.utcnow()
            published = now.strftime(
                '%Y-%m-%d') if (':' in i('li.zhhf').html().strip()) else i('li.zhhf').html().strip()
            now = now.strftime('%Y-%m-%dT%H:%M:%SZ')

            if published < deadline:
                return

            yield dict(title=title, href=href, author=author, published=published, insert_dt=now)


def autohome_trace(model, deadline):
    URL_FORMAT = 'http://club.autohome.com.cn/bbs/forum-c-{model}-{page}.html?orderby=dateline&qaType=-1'
    BASE_URL = 'http://club.autohome.com.cn'
    for page in count(1):

        url = URL_FORMAT.format(page=page, model=model)
        logger.debug('autohome trace {url}'.format(url=url))
        content = get_content(url)
        d = pq(content)
        rows = d('dl.bluebg:last').nextAll('dl.list_dl')

        for row in rows:

            i = pq(row)
            title = i('dt a').html().strip()
            href = BASE_URL + i('dt a').attr('href')
            author = i('dd:eq(0) a').html()
            published = i('dd:eq(0) span.tdate').html()
            now = datetime.datetime.utcnow()
            now = now.strftime('%Y-%m-%dT%H:%M:%SZ')

            if published < deadline:
                return

            yield dict(title=title, href=href, author=author, published=published, insert_dt=now)


"""
def exit_func(published, deadline):
	if ':' in published:
		return False
	elif published < deadline:
		return True
	return False
"""


def feed_item(item):
    assert 'type' in item
    if item['type'] == 'autohome':
        parser = autohome_trace
    if item['type'] == 'bitauto':
        parser = bitauto_trace
    print list(parser(item['model'],'2015-08-08'))


rootdir = os.path.abspath(os.path.dirname(__file__))
public = os.path.join(rootdir, 'json')

def parse_bitauto():
    with open(os.path.join(public, 'bitauto.json')) as f:
        data = json.load(f)

    keys = data.keys()

    for key in keys:
        item = data[key]
        item['type'] = 'bitauto'
        yield item


def parse_autohome():
    with open(os.path.join(public, 'autohome.json')) as f:
        data = json.load(f)

    keys = data.keys()

    for key in keys:
        item = data[key]
        item['type'] = 'autohome'
        yield item  


def things():
    for item in parse_bitauto():
        yield item
    for item in parse_autohome():
        yield item

def main():
    pool = Pool(processes=4)
    rv = pool.map_async(feed_item, things())
    rv.wait()

if __name__ == '__main__':
    main()