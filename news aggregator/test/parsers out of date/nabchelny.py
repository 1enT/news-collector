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

class Nabchelny:
	def __init__(self, url = "", url_to_files = "supportive files"):
		self.url_to_files = url_to_files
		self.__current_new = {"time": datetime.strptime("11 февраль 2023 19:01", "%d %B %Y %H:%M"), 
			   "title": "Челнинцы развивают республиканское объединение детей и молодежи",
			   "lead": "Делегация из Набережных Челнов принимает участие на установочном семинаре «Движение первых».",
			   "link": "http://nabchelny.ru/news/50176",
			   "img_url": "http://nabchelny.ru/upload/news/2023/02/news_63e7bbdda2ec4/homephoto/img.jpg"}
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
		page = requests.get("http://nabchelny.ru", stream = True, headers = self.__cookies)
		soup = BeautifulSoup(page.content, "html.parser")
		last_one = soup.find_all(attrs={"class", "span7"})[1].find(attrs={"class", "main-news-list"})

		time = self.__get_date(last_one.find(attrs={"class": "news-list-body"}).span.contents[0])
		title = last_one.find(attrs={"class": "news-list-body"}).a.string
		lead = last_one.find(attrs={"class": "news-list-body"}).contents[2].replace('\n', '').strip()
		link = "http://nabchelny.ru" + last_one.find(attrs={"class": "news-list-body"}).a.get('href')
		img_url = last_one.find('img')
		if img_url != None:
			img_url = "http://nabchelny.ru" + img_url.get('src')
		self.__current_new = {"source": "Наб. Челны", "time": time, "title": title, "lead": lead, "link": link, "img_url": img_url}

	def find_last_news(self):
		page = requests.get("http://nabchelny.ru", stream = True, headers = self.__cookies)
		soup = BeautifulSoup(page.content, "html.parser")
		list_of_news = soup.find_all(attrs={"class", "span7"})[1].find_all(attrs={"class", "main-news-list"})
		
		for each_new in list_of_news:
			time = self.__get_date(each_new.find(attrs={"class": "news-list-body"}).span.contents[0])
			if self.__current_new['time'] < time:
				title = each_new.find(attrs={"class": "news-list-body"}).a.string
				lead = each_new.find(attrs={"class": "news-list-body"}).contents[2].replace('\n', '').strip()
				link = "http://nabchelny.ru" + each_new.find(attrs={"class": "news-list-body"}).a.get('href')
				text = json.dumps(self.__parse_news_body(link), ensure_ascii=False).encode('utf8').decode()
				img_url = each_new.find('img')
				if img_url != None:
					img_url = "http://nabchelny.ru" + img_url.get('src')
				if title == self.__current_new['title']:
					break
				self.last_news.append({"source": "nabchelny", "time": time, "title": title, "lead": lead, "text": "", "link": link, "img_url": img_url})
			else:
				break

		if len(self.last_news) > 0:
			self.__current_new = self.last_news[0]

	def __parse_news_body(self, url):
		page = requests.get(url, stream = True, headers = self.__cookies)
		soup = BeautifulSoup(page.content, "html.parser")
		content = soup.find(attrs={"class": "news_story"})
		# content_text = []
		# for i in content.children:
		# 	print(i)
		# 	if i.replace('\n', '') != '' and i.replace(' ', '') != '':
		# 		content_text.append(i) 
		content_text = [i for i in content.children if i != '\n' and i != ' ']
		#print(content_text)

		parsed_content = []
		for item in content_text:
			#is_img = [i for i in item.descendants if i.name == "img"]
			#if len(is_img) != 0:
			img = item.find('img')
			if img != -1 and img is not None:
				img_src = img['src']
				parsed_tag = {
						"type": "img",
						"src": "https://nabchelny.ru{}".format(img_src),
						"children": [{"text": ""}]
					}
				parsed_content.append(parsed_tag)
			#else:
			if item.text.replace('\n', '').replace('\r', '') != '':
				parsed_tag = {
							"type": "plain",
							"text": item.text.replace('\n', '').replace('\r', '')
						}
				parsed_content.append(parsed_tag)
			# elif item.name == 'p':
			# 	parsed_paragraph = self.__recursive_children_search(item)
			# 	parsed_tag = {
			# 			"type": "p",
			# 			"children": parsed_paragraph
			# 		}
			# 	if parsed_tag['children'] == []:
			# 		continue
			# 	parsed_content.append(parsed_tag)
			# else:
			# 	for item_2 in item.children:
			# 		if item_2.name == 'p':
			# 			parsed_paragraph = self.__recursive_children_search(item_2)
			# 			parsed_tag = {
			# 					"type": "p",
			# 					"children": parsed_paragraph
			# 				}
			# 			if parsed_tag['children'] == []:
			# 				continue
			# 			parsed_content.append(parsed_tag)

		return parsed_content

	def __recursive_children_search(self, tag):
		parsed_tag = []

		for piece in tag.children:
			if isinstance(piece, bs4.element.NavigableString):
				parsed_piece = {
					"type": "plain",
					"text": piece.text.replace('\n', '').replace('\r', '')
				}
				parsed_tag.append(parsed_piece)
			else:
				if piece.name == 'a':
					# parsed_piece = {
					# 	"type": "a",
					# 	"href": piece['href'],
					# 	"children": self.__recursive_children_search(piece)
					# }
					parsed_piece = {
						"type": "a",
						"href": piece["href"],
						"text": piece.text
					}

				if piece.name == 'b' or piece.name == 'strong':
					# parsed_piece = {
					# 	"type": "bold",
					# 	"children": self.__recursive_children_search(piece)
					# }
					parsed_piece = {
						"type": "plain",
						"bold": "true",
						"text": piece.text
					}

				if piece.name == 'i' or piece.name == 'em':
					# parsed_piece = {
					# 	"type": "cursive",
					# 	"children": self.__recursive_children_search(piece)
					# }
					parsed_piece = {
						"type": "plain",
						"cursive": "true",
						"text": piece.text
					}

				if piece.name == 'br':
					continue

				if piece.name == 'span':
					parsed_tag += self.__recursive_children_search(piece)
				else:
					#print(piece)
					parsed_tag.append(parsed_piece)
		return parsed_tag

	def get_last_news(self):
		news = copy.deepcopy(self.last_news)
		for i in range(len(news)):
			news[i]['time'] = self.__prettify_date(news[i]['time'])
		return news

	def drop_last_news(self):
		self.last_news = deque()

	def __get_date(self, text):
		text = text.replace('\n', '').strip()
		# date = re.search(r"\d{2} [а-яА-Я]+ \d{4}", text)[0].split()
		# time = re.search(r"\d\d:\d\d", text)[0]
		text = text.split(',')
		date = text[1].split()
		time = text[2].strip()
		with open(f"{self.url_to_files}/russian_months.json", encoding='utf8') as file:
			months = json.loads(file.read())
			date = ' '.join([date[0], months[date[1]], date[2]]) + f" {time}"
		return datetime.strptime(date, "%d %B %Y %H:%M")

	def __prettify_date(self, date):
		return date.strftime('%Y-%m-%d %H:%M')

	def current_new(self):
		return self.__current_new
		
if __name__ == "__main__":
	parser = Nabchelny()

	parser.fix_last_new()
	parser.find_last_news()
	print(parser.last_news)
	print(parser._Nabchelny__current_new)