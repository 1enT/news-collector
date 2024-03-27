#from parsers.IParser import IParser

import requests
from bs4 import BeautifulSoup
import bs4
from collections import deque
import re
import json
import copy

from datetime import datetime, date

class Pra_Parser:
	def __init__(self, url, source, get_date, prettify_date):
		self.url = url
		self.source = source
		self.url_to_files = "supportive files"
		self.url_to_russian_months = ""
		self.last_news = deque()
		self._cookies = {
								'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
								'accept-encoding': 'gzip, deflate, br',
								'accept-language': 'ru-RU,ru;q=0.9',
								'cache-control': 'max-age=0',
								'cookie': 'DNSID=4252b2d99455b43d677997b13ea39c6e065b7893; design=ad; cookieAgree=true; session-cookie=173fa94b7d4d8a379543040abeb261f59d78cb00aaafd8f9482ab26fc7606dec25bf5b2e2b14c89d4c2505e3b5a9fee6',
								'sec-fetch-dest': 'document',
								'sec-fetch-mode': 'navigate',
								'sec-fetch-site': 'none',
								'sec-fetch-user': '?1',
								'sec-gpc': '1',
								'upgrade-insecure-requests': '1',
								'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
						 }

		self._get_date = get_date
		self._prettify_date = prettify_date

	def _sup_fix_last_new(self, 
							last_one, selector_time, selector_title, selector_lead, selector_link, selector_img_url
							):
		time = self._get_date(last_one.select(selector_time)[0].contents)
		title = last_one.select(selector_title)[0].string.strip()
		link = last_one.select(selector_link)[0].get('href')
		img_url = last_one.select(selector_img_url)[0]
		if img_url != None:
			img_url = img_url.get('src')
		self.__current_new = {"source": self.source, "time": time, "title": title, "lead": "", "link": link, "img_url": img_url}

	def _sup_find_last_news(self, 
							list_of_news, selector_time, selector_title, selector_lead, selector_link, selector_img_url
							):
		for i, each_new in enumerate(list_of_news):
			time = self._get_date(each_new.select(selector_time)[0].contents)
			if self._current_new['time'] < time:
				title = each_new.select(selector_title)[0].string.strip()
				link = each_new.select(selector_link)[0].get('href')
				text = json.dumps(self.__parse_news_body(link), ensure_ascii=False).encode('utf8').decode()
				img_url = each_new.select(selector_img_url)[0]
				if img_url != None:
					img_url = img_url.get('src')
				if title == self._current_new['title']:
					break
				self.last_news.append({"source": self.source, "time": time, "title": title, "lead": "", "text": text, "link": link, "img_url": img_url})
			else:
				break

		if len(self.last_news) > 0:
			self._current_new = self.last_news[0]

	def __parse_news_body(self):
		pass

	def _sup_get_last_news(self):
		news = copy.deepcopy(self.last_news)
		for i in range(len(news)):
			news[i]['time'] = self._prettify_date(news[i]['time'])
		return news

	def _sup_drop_last_news(self):
		self.last_news = deque()

	def _sup_current_new(self):
		return self._current_new