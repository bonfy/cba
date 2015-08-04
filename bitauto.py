#!/usr/bin/env python
# coding: utf-8

"""
    cba
    ~~~~~~~
    car bbs analyse
    :copyright: (c) 2015 by Bonfy.
"""

__version__ = '0.1'
__author__ = 'Bonfy <foreverbonfy@163.com>'

import requests
from pyquery import PyQuery as pq
from config import USER_AGENTS, logger
import random
import datetime

# BASE_URL='http://baa.bitauto.com'

# step 1 connect to the url
# step 2 juge encoding and change to gbk
# step 3 use pyquery to get information we need


url = 'http://baa.bitauto.com/langjing/index-all-all-1-1.html'
r = requests.get(url, headers={'User-Agent': random.choice(USER_AGENTS)})
assert r.status_code == 200

if r.encoding in ('ISO-8859-1', 'gb2312'):
	logger.debug('Turn coding from {coding} to gbk'.format(coding=r.encoding))
	r.encoding = 'gbk'

content = r.text

d = pq(content)
rows = d('div.postslist_xh')

for row in rows:
         i = pq(row)
         title = i('li.bt span').text().strip()
         href = i('li.bt a').attr('href')
         author = i('li.zz a').html().strip()
         published = i('li.zhhf').html().strip()
         now = datetime.datetime.utcnow()
         now = now.strftime('%Y-%m-%dT%H:%M:%SZ')
         print title, href, author, published, now