# coding: utf-8


import requests
from pyquery import PyQuery as pq
from config import USER_AGENTS, logger
import random
import datetime
import json


#'http://baa.bitauto.com/{model}/index-all-all-{page}-1.html'
#'http://club.autohome.com.cn/bbs/forum-c-{model}-{page}.html?orderby=dateline&qaType=-1',

def get_content(url):

	r = requests.get(url, headers={'User-Agent': random.choice(USER_AGENTS)})
	assert r.status_code == 200
	if r.encoding in ('ISO-8859-1', 'gb2312'):
		logger.debug('Turn coding from {coding} to gbk'.format(coding=r.encoding))
		r.encoding = 'gbk'
	return r.text


def bitauto_trace( lst, model, page, url_format , deadline):
	
	url = url_format.format(page=page,model=model)
	print url
	content = get_content(url)

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
		
		print dict(title=title,href=href,author=author,published=published,insert_dt=now)
		lst.append(dict(title=title,href=href,author=author,published=published,insert_dt=now))

	return autohome_trace(lst,model,page,url_format,deadline)


def autohome_trace( lst, model, page, url_format, deadline):

	BASE_URL='http://club.autohome.com.cn'

	url = url_format.format(page=page,model=model)
	content = get_content(url)
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

		if exit_func(published):
			return lst
		lst.append(dict(title=title,href=href,author=author,published=published,insert_dt=now))

	return autohome_trace(lst,model,page,url_format,deadline)

"""
def exit_func(published, deadline):
	if ':' in published:
		return False
	elif published < deadline:
		return True
	return False
"""

def feed_item(item):
	pass

def parse_item():

	with open('model.json') as f:
		data = json.load(f)

	keys = data.keys()

	for key in keys:
		item = data[key]
		yield item

