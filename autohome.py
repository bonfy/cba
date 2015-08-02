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

BASE_URL='http://club.autohome.com.cn'

# step 1 connect to the url
# step 2 juge encoding and change to gbk
# step 3 use pyquery to get information we need


url = 'http://club.autohome.com.cn/bbs/brand-1-c-145-1.html?type=None&sort=Lastest'
r = requests.get(url, headers={'User-Agent': random.choice(USER_AGENTS)})
assert r.status_code == 200

if r.encoding in ('ISO-8859-1', 'gb2312'):
	logger.debug('Turn coding from {coding} to gbk'.format(coding=r.encoding))
	r.encoding = 'gbk'

content = r.text

d = pq(content)
rows = d('dl.list_dl')[1:]

for row in rows:
	i = pq(row)
	title = i('dt a').html().strip()
	href = BASE_URL + i('dt a').attr('href')
	author = i('dd:eq(0) a').html()
	published = i('dd:eq(0) span.tdate').html()
	now = datetime.datetime.utcnow()
	now = now.strftime('%Y-%m-%dT%H:%M:%SZ')
	print title , href , author ,published ,now



