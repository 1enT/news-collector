import requests
from bs4 import BeautifulSoup
from collections import deque
import re
import json
import copy
import time

from datetime import datetime, date
import locale
locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))

class Tatar_inform:
	def __init__(self, url = "", url_to_files = "supportive files"):
		self.url_to_files = url_to_files
		self.__current_new = {"time": datetime.strptime("15 февраль 2023", "%d %B %Y"),
			   "title": "«Будут покемоны и НЛО»: Захарова ответила на сообщения властей США о внеземных объектах",
			   "lead": "",
			   "link": "https://www.tatar-inform.ru/news/budut-pokemony-i-nlo-zaxarova-otvetila-na-soobshheniya-vlastei-ssa-o-vnezemnyx-obektax-5896657",
			   "img_url": None}
		self.last_news = deque()
		self.__cookies = {
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

	def fix_last_new(self):
		page = requests.get("https://www.tatar-inform.ru/news", stream = True, headers = self.__cookies)
		soup = BeautifulSoup(page.content, "html.parser")
		last_one = soup.find(attrs={"class", "newsList__list"}).find(attrs={"class", "newsList__item"})

		time = self.__get_date(last_one.find(attrs={"class":"newsList__item-date"}).contents)
		title = last_one.find(attrs={"class":"newsList__item-title"}).string.strip()
		link = last_one.find(attrs={"class":"newsList__item-text"}).get('href')
		img_url = last_one.find('img')
		if img_url != None:
			img_url = img_url.get('src')
		self.__current_new = {"source": "tatar-inform", "time": time, "title": title, "lead": "", "link": link, "img_url": img_url}

	def find_last_news(self):
		page = requests.get("https://www.tatar-inform.ru/news", stream = True, headers = self.__cookies)
		soup = BeautifulSoup(page.content, "html.parser")
		list_of_news = soup.find(attrs={"class", "newsList__list"}).find_all(attrs={"class", "newsList__item"})

		for i, each_new in enumerate(list_of_news):
			time = self.__get_date(each_new.find(attrs={"class":"newsList__item-date"}).contents)
			if self.__current_new['time'] <= time:
				title = each_new.find(attrs={"class":"newsList__item-title"}).string.strip()
				link = each_new.find(attrs={"class":"newsList__item-text"}).get('href')
				img_url = each_new.find('img')
				if img_url != None:
					img_url = img_url.get('src')
				if title == self.__current_new['title']:
					break
				self.last_news.append({"source": "tatar-inform", "time": time, "title": title, "lead": "", "text": "", "link": link, "img_url": img_url})
			else:
				break

		if len(self.last_news) > 0:
			self.__current_new = self.last_news[0]

	def get_last_news(self):
		news = copy.deepcopy(self.last_news)
		for i in range(len(news)):
			news[i]['time'] = self.__prettify_date(news[i]['time'])
		return news

	def drop_last_news(self):
		self.last_news = deque()

	def __get_date(self, text):
		text.pop(1)
		text = ''.join(text).replace('\n', '').strip()
		date = re.search(r"\d+ [а-яА-Я]+ \d{4}", text)[0].split()
		time = re.search(r"\d\d:\d\d", text)[0]
		with open(f"{self.url_to_files}/russian_months.json", encoding='utf8') as file:
			months = json.loads(file.read())
			date = ' '.join([date[0], months[date[1]], date[2]]) + f" {time}"
		return datetime.strptime(date, "%d %B %Y %H:%M")

	def __prettify_date(self, date):
		return date.strftime('%Y-%m-%d %H:%M')

	def current_new(self):
		return self.__current_new


if __name__ == "__main__":
	parser = Tatar_inform()
	parser.fix_last_new()
	#parser.find_last_news()
	#print(parser.current_new())
	#print(parser._Tatar_inform__current_new)
	print(parser.current_new())
	print('-----------------------------------------------------')
	print('-----------------------------------------------------')
	for i in range(240):
		parser.find_last_news()
		if len(parser.get_last_news()) > 0:
			print(parser.get_last_news())
			print('-----------------------------------------------------')
			parser.drop_last_news()
		time.sleep(30)