
#from parsers.Parser import Pra_Parser

import requests
from bs4 import BeautifulSoup
import bs4
from collections import deque
import re
import json
import copy

from datetime import datetime, date

import locale
locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))

class Rais:
	def __init__(self, url = "", url_to_files=""):
		self.__current_new = {"time": datetime.strptime("10 февраль 2023", "%d %B %Y"), 
			   "title": "Рустам Минниханов в Альметьевске принял участие в открытии нового детсада в микрорайоне «Алсу»",
			   "lead": "С рабочей поездкой в Альметьевском муниципальном районе находится сегодня Раис Республики Татарстан Рустам Минниханов. Основная цель – участие в заседании Совета Альметьевского муниципального района и Альметьевского городского Совета «Об итогах социально-экономического развития Альметьевского муниципального района за 2022 год и задачах на 2023 год».",
			   "link": "https://rais.tatarstan.ru/index.htm/index.htm/news/2166288.htm",
			   "img_url": None}
		self.last_news = deque()
		self.source = "Раис"
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
		page = requests.get("https://rais.tatarstan.ru/index.htm/news?format=json&limit=15&page=1", stream = True, headers = self.__cookies)
		data = json.loads(page.text)

		last_one = data['items'][0]
		time = datetime.strptime(last_one['news_date'], "%Y-%m-%d")
		title = last_one['title']
		lead = BeautifulSoup(last_one['lead'], "html.parser").string
		link = "https://rais.tatarstan.ru" + last_one['url']

		self.__current_new = {"source": self.source, "time": time, "title": title, "lead": lead, "link": link, "img_url": None}

	def find_last_news(self):
		page = requests.get("https://rais.tatarstan.ru/index.htm/news?format=json&limit=15&page=1", stream = True, headers = self.__cookies)
		data = json.loads(page.text)

		for per_new in data['items']:
			time = datetime.strptime(per_new['news_date'], "%Y-%m-%d")
			if self.__current_new['time'] < time:
				title = per_new['title']
				lead = BeautifulSoup(per_new['lead'], "html.parser").string
				#text = self.__parse_news_body(per_new)
				text = json.dumps(self.__parse_news_body(link), ensure_ascii=False).encode('utf8').decode()
				link = "https://rais.tatarstan.ru" + per_new['url']
				if title == self.__current_new['title']:
					break
				if per_new['image_file_big'] != None:
					img_url = 'https://rais.tatarstan.ru' + per_new['image_file_big']
				else:
					img_url = None
				# else:
				# 	if per_new['photoreport']['url'] != None:
				# 		num = re.search(r"\d+", per_new['photoreport']['url'])[0]
				# 		page = requests.get('https://rais.tatarstan.ru/index.htm/news/?format=json&export=photos&measure_id=' + num, stream = True, headers = self.__cookies)
				# 		data = json.loads(page.text)
				# 		img_url = 'http://rais.tatarstan.ru' + data['items'][1]['image_view']
				# 	else:
				# 		img_url = None
				self.last_news.append({"source": self.source, "time": time, "title": title, "lead": lead, "text": text, "link": link, "img_url": img_url})
			else:
				break

		if len(self.last_news) > 0:
			self.__current_new = self.last_news[0]

	def __parse_news_body(self, new):
		soup = BeautifulSoup(new['text'], "html.parser")
		
		parsed_content = []
		is_there_img = new['image_file_big']
		if is_there_img is not None:
			parsed_tag = {
					"type": "img",
					"src": 'https://rais.tatarstan.ru' + new['image_file_big'],
					"children": [{"text": ""}]
				}
			parsed_content.append(parsed_tag)
		for item in soup.children:
			parsed_paragraph = self.__children_search(item)
			parsed_tag = {
				"type": "p",
				"children": parsed_paragraph
			}
			parsed_content.append(parsed_tag)

		return parsed_content

	def __children_search(self, tag):
		parsed_tag = []

		for piece in tag.children:
			if isinstance(piece, bs4.element.NavigableString):
				parsed_piece = {
					"type": "plain",
					"text": piece.text
				}
				parsed_tag.append(parsed_piece)
			else:
				if piece.name == 'a':
					parsed_piece = {
						"type": "a",
						"href": piece["href"],
						"text": piece.text
					}

				if piece.name == 'b' or piece.name == 'strong':
					parsed_piece = {
						"type": "plain",
						"bold": "true",
						"text": piece.text
					}

				if piece.name == 'i' or piece.name == 'em':
					parsed_piece = {
						"type": "plain",
						"cursive": "true",
						"text": piece.text
					}
				parsed_tag.append(parsed_piece)
		return parsed_tag

	def get_last_news(self):
		news = copy.deepcopy(self.last_news)
		for i in range(len(news)):
			news[i]['time'] = self.__prettify_date()
		return news

	def drop_last_news(self):
		self.last_news = deque()

	def current_new(self):
		return self.__current_new

	def __prettify_date(self):
		now = datetime.now().strftime('%Y-%m-%d %H:%M')
		return now

if __name__ == "__main__":
	parser = Rais()
	#parser.fix_last_new()
	parser.find_last_news()
	print(parser.last_news)
	#print(parser._Rais__current_new)