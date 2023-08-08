# parser = Parse("https://sovmo.tatarstan.ru")
# Parser.day - день в новостях
# iter Parser - выдает по одной новости текущего дня
# Parser.all_day_news() - новости всего дня
# Parser.manual_parse() - заново парсит новости со страницы


import requests
from bs4 import BeautifulSoup
import json
import locale
from datetime import datetime, date
import pprint

locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))

class Parse:
	def __init__(self, url, pres=False):
		self.url = url
		self.news_of_the_day = {}
		self.day = -1
		self.num_day = 0
		self.num_page = 1
		self.pres = pres
		self.cookies = {
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
		self.__start_parcing()
		self.iter_num_new = -1

	def get_image(self):
		if self.pres:
			for each_new in self.news_of_the_day:
				page = requests.get(each_new['link'] + '?format=json', stream = True, headers = self.cookies)
				data = json.loads(page.text)
				if data['items']['image_file_big'] is not None:
					each_new['img'] = 'https://rais.tatarstan.ru' + data['items']['image_file_big']
				else:
					if data['items']['photoreport']['url'] is not None:
						num = data['items']['photoreport']['url'].replace('.htm', '').replace('/pressa/photoreports/photoreport/', '')
						page = requests.get('https://rais.tatarstan.ru/index.htm/news/?format=json&export=photos&measure_id=' + num, stream = True, headers = self.cookies)
						data = json.loads(page.text)
						each_new['img'] = 'http://rais.tatarstan.ru' + data['items'][1]['image_view']
					else:
						each_new['img'] = None
		else:
			for each_new in self.news_of_the_day:
				page = requests.get(each_new['link'], stream = True, headers = self.cookies)
				soup = BeautifulSoup(page.text, "html.parser")
				img = soup.find(attrs={'class': 'article__photo'}).find('img')
				if img is None:
					img = None
				else:
					img = img.get('src')
				each_new['img'] = img


	def manual_parse(self):
		self.__start_parcing()

	def all_day_news(self):
		return self.news_of_the_day

	def __start_parcing(self):
		if self.pres:
			self.__parse_pres_site()
		else:
			self.__parse_common_sites()
		self.news_of_the_day = self.news_of_the_day[self.day]
		self.news_of_the_day.reverse()

	def __parse_common_sites(self):
		page = requests.get(self.url + "/index.htm/news/tape?page={}".format(self.num_page), stream = True, headers = self.cookies)
		soup = BeautifulSoup(page.text, "html.parser")
		list_of_news = soup.body.div.find(attrs={'class': 'content'}).find(attrs={'class': 'container-fluid'}).find(attrs={'class': 'row'}).find(attrs={'class': 'content__main'}).find(attrs={'class': 'list'}).find_all(attrs={'class': 'row'})

		one_row = self.__get_contents(list_of_news[0])

		date, news = one_row
		day = date.find(attrs={'class': 'day-month__date'}).string.replace('\n', '').strip()
		month_year = date.find(attrs={'class': 'day-month__row'}).string.replace('\n', '').strip()
		date = '{} {}'.format(day, month_year)
			
		self.news_of_the_day.update({date: []})
		self.day = date
		for per_new in self.__get_contents(news):
			per_new = per_new.find(attrs={'class': 'list__item'})
			title = per_new.find(attrs={'class': 'list__title'}).find('a').string.replace('\xa0', '').strip()
			text = per_new.find(attrs={'class': 'list__text'}).find('p').string.replace('\xa0', '').strip()
			link = self.url + per_new.find(attrs={'class': 'list__title'}).find('a').get('href')
				
			self.news_of_the_day[date].append({"title": title, "text": text, "link": link})

	def __parse_pres_site(self):
		page = requests.get(self.url + "/index.htm/news?format=json&limit=15&page=1", stream = True, headers = self.cookies)
		data = json.loads(page.text)

		for per_new in data['items']:
			title = per_new['title']
			text = BeautifulSoup(per_new['lead'], "html.parser").string
			link = self.url + per_new['url']
			date = datetime.strptime(per_new['news_date'], '%Y-%m-%d').strftime('%d %B %Y')
			
			if self.day == -1:
				self.news_of_the_day.update({date: []})
				self.day = date
			elif self.day != date:
				break
			self.news_of_the_day[date].append({"title": title, "text": text, "link": link})

	def __get_contents(self, tag):
		childs = tag.contents.copy()
		while '\n' in childs:
			childs.remove('\n')
		return childs

	def __next__(self): # Выдает по одной новости текущего дня
		self.iter_num_new += 1
		if self.iter_num_new < len(self.news_of_the_day):
			return self.news_of_the_day[self.iter_num_new]
		else:
			self.iter_num_new = -1
			raise StopIteration

	def __iter__(self):
		return self
