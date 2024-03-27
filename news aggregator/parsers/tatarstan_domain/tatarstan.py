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

class Tatarstan:
	def __init__(self, url, source):
		self.url = url
		self.source = source

		self.__current_new = {"time": datetime.strptime("10 февраль 2023", "%d %B %Y"), 
			   "title": "Рустам Минниханов в Альметьевске принял участие в открытии нового детсада в микрорайоне «Алсу»",
			   "lead": "С рабочей поездкой в Альметьевском муниципальном районе находится сегодня Раис Республики Татарстан Рустам Минниханов. Основная цель – участие в заседании Совета Альметьевского муниципального района и Альметьевского городского Совета «Об итогах социально-экономического развития Альметьевского муниципального района за 2022 год и задачах на 2023 год».",
			   "link": "https://rais.tatarstan.ru/index.htm/news/2166288.htm",
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

	def set_sup_files_url(self, url):
		self.url_to_files = url

	def fix_last_new(self):
		page = requests.get(self.url + "/index.htm/news", stream = True, headers = self.__cookies)
		soup = BeautifulSoup(page.content, "html.parser")
		last_one = soup.find(attrs={'class': 'list'}).find(attrs={'class': 'row'})
		
		time = self.__get_date(
			last_one.find(attrs={"class": "day-month__date"}).string.strip() + " " + 
			last_one.find(attrs={"class": "day-month__row"}).string.strip()
			)
		very_last_one = last_one.find(attrs={"class": "list__item"})
		title = very_last_one.find(attrs={"class": "list__title"}).a.string.replace('\xa0', '').strip()
		#lead = very_last_one.find(attrs={"class": "list__text"}).p.string.replace('\xa0', '').strip()
		lead = very_last_one.find(attrs={"class": "list__text"}).text.replace('\xa0', '').strip()
		link = self.url + very_last_one.find(attrs={"class": "list__title"}).a.get('href')
				
		self.__current_new = {"time": time, "title": title, "lead": lead, "link": link, "img_url": None}

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
					lead = each_new.find(attrs={"class": "list__text"}).text.replace('\xa0', '').strip()
					link = self.url + each_new.find(attrs={"class": "list__title"}).a.get('href')
					text = json.dumps(self.__parse_news_body(link), ensure_ascii=False).encode('utf8').decode()
					self.last_news.append({"source": self.source, "time": time, "title": title, "lead": lead, "text": text, "link": link, "img_url": None})
			else:
				break

		if len(self.last_news) > 0:
			self.__current_new = self.last_news[0]

	def test_parse(self, link):
		text = json.dumps(self.__parse_news_body(link), ensure_ascii=False).encode('utf8').decode()
		return text

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

		i, j = 0, 0
		while True:
			if len(parsed_content) <= i:
				break

			if parsed_content[i]['type'] == 'p':
				while True:
					if len(parsed_content[i]['children']) <= j:
						break

					is_left = False
					is_right = False
					if j == 0:
						parsed_content[i]['children'][j]['text'] = parsed_content[i]['children'][j]['text'].lstrip()
					if j == len(parsed_content[i]['children'])-1:
						parsed_content[i]['children'][j]['text'] = parsed_content[i]['children'][j]['text'].rstrip()
					piece = parsed_content[i]['children'][j]
					
					if {'href', 'bold', 'cursive', 'underline'} & set(piece):
						if piece['text'].lstrip() != piece['text']:
							parsed_content[i]['children'][j]['text'] = piece['text'].lstrip()
							prev_piece = parsed_content[i]['children'][j-1]
							if not {'href', 'bold', 'cursive', 'underline'} & set(prev_piece):
								parsed_content[i]['children'][j-1]['text'] = prev_piece['text'] + ' '
							else:
								is_left = True
								parsed_content[i]['children'].insert(j, {
									"type": "plain",
									"text": ' '
								})
								j += 1
						if piece['text'].rstrip() != piece['text']:
							parsed_content[i]['children'][j]['text'] = piece['text'].rstrip()
							next_piece = parsed_content[i]['children'][j+1]
							if not {'href', 'bold', 'cursive', 'underline'} & set(next_piece):
								parsed_content[i]['children'][j+1]['text'] = ' ' + next_piece['text']
							else:
								is_right = True
								parsed_content[i]['children'].insert(j+1, {
									"type": "plain",
									"text": ' '
								})


					if parsed_content[i]['children'][j]['text'] == '':
						parsed_content[i]['children'].pop(j)
						j -= 1
					j += 1+2*int(is_right)
				if len(parsed_content[i]['children']) == 0:
					parsed_content.pop(i)
					i -= 1
			i += 1
			j = 0

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

	def get_last_news(self):
		news = copy.deepcopy(self.last_news)
		for i in range(len(news)):
			news[i]['time'] = self.__prettify_date()
		return news

	def drop_last_news(self):
		self.last_news = deque()

	def current_new(self):
		return self.__current_new

	def get_source(self):
		return self.source

	def __get_date(self, text):
		date = re.search(r"\d+ [а-яА-Я]+ \d{4}", text)[0].split()
		with open(f"{self.url_to_files}/russian_months.json", encoding='utf8') as file:
			months = json.loads(file.read())
			date = ' '.join([date[0], months[date[1]], date[2]])
		return datetime.strptime(date, "%d %B %Y")

	def __prettify_date(self):
		now = datetime.now().strftime('%Y-%m-%d %H:%M')
		return now