import requests
from bs4 import BeautifulSoup
import bs4
import json
import re
from collections import deque

import datetime
import locale
locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))

from test_db_connect import DatabaseProducer

class Sov_gos_prav:
	def __init__(self, url):
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
		self.last_news = deque()
		self.source = "Сармановский"

		self.url = url
		self.url_to_files = "supportive files"
		#"C:\Users\LkzCt\OneDrive\Документы\Работа\news collector\news aggregator\test\supportive files\russian_months.json"

	def set_current_new(self, obj):
		self.__current_new = obj

	def current_new(self):
		return self.__current_new

	def find_last_news(self):
		page = requests.get(self.url + "/index.htm/news", stream = True, headers = self.__cookies)
		soup = BeautifulSoup(page.content, "html.parser")
		list_of_news = soup.find(attrs={'class': 'list'}).find_all(attrs={'class': 'row'})
		
		for one_day in list_of_news:
			time = self.__get_date(
				one_day.find(attrs={"class": "day-month__date"}).string.strip() + " " + 
				one_day.find(attrs={"class": "day-month__row"}).string.strip()
				)

			if self.__current_new['time'] <= time:
				for each_new in one_day.find_all(attrs={"class": "list__item"}):
					title = each_new.find(attrs={"class": "list__title"}).a.string.replace('\xa0', '').strip()
					if title == self.__current_new['title']:
						break
					lead = each_new.find(attrs={"class": "list__text"}).p.string.replace('\xa0', '').strip()
					link = self.url + each_new.find(attrs={"class": "list__title"}).a.get('href')
					#text = json.dumps(self.__parse_news_body(link), ensure_ascii=False).encode('utf8').decode()
					text = "123"
					self.last_news.append({"source": self.source, "time": time, "title": title, "lead": lead, "text": text, "link": link, "img_url": None})
			else:
				break

		if len(self.last_news) > 0:
			self.__current_new = self.last_news[0]

	def __get_date(self, text):
		date = re.search(r"\d+ [а-яА-Я]+ \d{4}", text)[0].split()
		with open(f"{self.url_to_files}/russian_months.json", encoding='utf8') as file:
			months = json.loads(file.read())
			date = ' '.join([date[0], months[date[1]], date[2]])
		return datetime.datetime.strptime(date, "%d %B %Y")

	def __parse_news_body(self, url):
		page = requests.get(url, stream = True, headers = self.__cookies)
		soup = BeautifulSoup(page.content, "html.parser")
		content = soup.find(attrs = {"class": "article"})
		content_overview = content.find(attrs = {"class": "article__photo-photo"})
		content_text = [item for item in content.children if item.name == "p"]

		is_there_wysiwyg = content.find(attrs = {"class": "wysiwyg"})
		if is_there_wysiwyg is not None:
			content_text = is_there_wysiwyg.contents

		parsed_content = []
		if content_overview is not None:
			content_overview = content_overview.find('img')['src']
			parsed_content.append(
				{
					"type": "img",
					"src": content_overview,
					"children": [{"text": ""}]
				}
			)

		for item in content_text:
			# if item.name == 'p':
			# 	parsed_paragraph = self.__recursive_children_search(item)
			# 	parsed_tag = {
			# 			"type": "p",
			# 			"children": parsed_paragraph
			# 		}
			# 	parsed_content.append(parsed_tag)
			if item.find('img') is not None and item.find('img') != -1:
				parsed_tag = {
						"type": "img",
						"src": self.url + item.find('img')['src'],
						"children": [{"text": ""}]
					}
				parsed_content.append(parsed_tag)
			elif item.name == 'p':
				parsed_paragraph = self.__recursive_children_search(item)
				parsed_tag = {
						"type": "p",
						"children": parsed_paragraph
					}
				parsed_content.append(parsed_tag)

		return parsed_content

	def __recursive_children_search(self, tag):
		parsed_tag = []

		for piece in tag.children:
			if isinstance(piece, bs4.element.NavigableString):
				parsed_piece = {
					"type": "plain",
					"text": piece.text.replace('\n', '').replace('\r', '')#.replace(u'\xa0', u'').replace(u'\x2009', '')
				}
				parsed_tag.append(parsed_piece)
			else:
				if piece.contents == []:
					continue
				if piece.name == 'a'and 'href' in piece:
					parsed_piece = {
						"type": "a",
						"href": piece["href"],
						"text": piece.text
					}

				elif piece.name == 'b' or piece.name == 'strong':
					parsed_piece = {
						"type": "plain",
						"bold": "true",
						"text": piece.text
					}

				elif piece.name == 'i' or piece.name == 'em':
					parsed_piece = {
						"type": "plain",
						"cursive": "true",
						"text": piece.text
					}

				elif piece.name == 'u':
					parsed_piece = {
						"type": "plain",
						"underline": "true",
						"text": piece.text
					}

				elif piece.name == 'a' and 'href' not in piece:
					parsed_piece = {
						"type": "plain",
						"text": piece.text
					}

				else:
					parsed_piece = {
						"type": "plain",
						"text": piece.text
					}

				if piece.name == 'span':
					parsed_tag += self.__recursive_children_search(piece)
				else:
					parsed_tag.append(parsed_piece)
		return parsed_tag

tatar = Sov_gos_prav("https://minzdrav.tatarstan.ru")
text = tatar._Sov_gos_prav__parse_news_body("https://mzio.tatarstan.ru/index.htm/news/2289396.htm")
text = json.dumps(text, ensure_ascii=False).encode('utf8').decode()
print(text)

# tatar = Sov_gos_prav("https://sarmanovo.tatarstan.ru")
# news = {'source': 'Сармановский', 'time': datetime.datetime(2023, 10, 24, 0, 0), 'title': 'День пожилых людей в клубе ветеранов п.г.т.Джалиль', 'lead': 'День пожилого человека – это добрый и светлый праздник, в который мы окружаем особым вниманием нашихбабушекидедушек.', 'text': '123', 'link': 'https://sarmanovo.tatarstan.ru/index.htm/news/2245461.htm', 'img_url': None}
# tatar.set_current_new(news)
# tatar.find_last_news()
# print(tatar.last_news)
# print()
# print(tatar.current_new())