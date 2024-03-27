import requests
from bs4 import BeautifulSoup
import bs4
from collections import deque
import re
import json
import copy
import time

from datetime import datetime, date
import locale
locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))

#from parsers.Parser import Pra_Parser

class Tatar_inform:
	def __init__(self):
		self.__current_new = {"time": datetime.strptime("15 февраль 2023", "%d %B %Y"),
			   "title": "«Будут покемоны и НЛО»: Захарова ответила на сообщения властей США о внеземных объектах",
			   "lead": "",
			   "link": "https://www.tatar-inform.ru/news/budut-pokemony-i-nlo-zaxarova-otvetila-na-soobshheniya-vlastei-ssa-o-vnezemnyx-obektax-5896657",
			   "img_url": None}
		self.last_news = deque()
		self.source = "Татар-информ"
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
		page = requests.get("https://www.tatar-inform.ru/news", stream = True, headers = self.__cookies)
		soup = BeautifulSoup(page.content, "html.parser")
		last_one = soup.find(attrs={"class", "newsList__list"}).find(attrs={"class", "newsList__item"})

		time = self.__get_date(last_one.find(attrs={"class":"newsList__item-date"}).contents)
		title = last_one.find(attrs={"class":"newsList__item-title"}).string.strip()
		link = last_one.find(attrs={"class":"newsList__item-text"}).get('href')
		img_url = last_one.find('img')
		if img_url != None:
			img_url = img_url.get('src')
		self.__current_new = {"source": self.source, "time": time, "title": title, "lead": "", "link": link, "img_url": img_url}

	def find_last_news(self):
		page = requests.get("https://www.tatar-inform.ru/news", stream = True, headers = self.__cookies)
		soup = BeautifulSoup(page.content, "html.parser")
		list_of_news = soup.find(attrs={"class", "newsList__list"}).find_all(attrs={"class", "newsList__item"})

		for i, each_new in enumerate(list_of_news):
			time = self.__get_date(each_new.find(attrs={"class":"newsList__item-date"}).contents)
			if self.__current_new['time'] < time:
				title = each_new.find(attrs={"class":"newsList__item-title"}).string.strip()
				link = each_new.find(attrs={"class":"newsList__item-text"}).get('href')
				text = json.dumps(self.__parse_news_body(link), ensure_ascii=False).encode('utf8').decode()
				# raw_text, text = self.__parse_news_body(link)
				# text = json.dumps(text, ensure_ascii=False).encode('utf8').decode()
				lead = self.__parse_news_lead(link)
				img_url = each_new.find('img')
				if img_url != None:
					img_url = img_url.get('src')
				if title == self.__current_new['title']:
					break
				# if lead != '':
				# 	raw_text = lead + '\n' + raw_text
				self.last_news.append({"source": self.source, "time": time, "title": title, "lead": lead, "text": text, "link": link, "img_url": img_url})
			else:
				break

		if len(self.last_news) > 0:
			self.__current_new = self.last_news[0]

	def __parse_news_lead(self, url):
		page = requests.get(url, stream = True, headers = self.__cookies)
		soup = BeautifulSoup(page.content, "html.parser")
		content = soup.find(attrs={"class": "main__news-lead"})
		lead = content.text
		if lead.replace(' ', '').replace('\n', '') == '':
			return ''
		else:
			return lead.replace('\n', '').strip()


	def __parse_news_body(self, url):
		page = requests.get(url, stream = True, headers = self.__cookies)
		soup = BeautifulSoup(page.content, "html.parser")
		content = soup.find(attrs={"class": "main__text"})
		content_overview = content.find(attrs={"class": "page-main__overview"})
		content_text = content.find(attrs={"class": "page-main__text"})
		content_embed_media = content.find(attrs={"class": "page-main__embed-media"})

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

		content_text = [i for i in content_text.children if i != '\n']
		for item in content_text:
			#is_img = [i for i in item.descendants if i.name == "img"]
			#if len(is_img) != 0:
			#if item.name == 'figure':
			img = item.find('img')
			if img != -1 and img is not None:
				img_src = img['src']
				parsed_tag = {
						"type": "img",
						"src": img_src,
						"children": [{"text": ""}]
					}
				parsed_content.append(parsed_tag)
			#elif item.name == 'p':
			else:
				parsed_paragraph = self.__parse_tags(item)
				parsed_tag = {
						"type": "p",
						"children": parsed_paragraph
					}
				if parsed_tag['children'] == []:
					continue
				parsed_content.append(parsed_tag)

		if content_embed_media is not None:
			content_embed_media = content_embed_media.find_all('img')
			for item in content_embed_media:
				parsed_content.append(
					{
						"type": "img",
						"src": item['data-splide-lazy'],
						"children": [{"text": ""}]
					}
				)

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


	def __parse_tags(self, tag):
		parsed_tag = []

		for piece in tag.children:
			piece_text = piece.text#.strip()
			if isinstance(piece, bs4.element.NavigableString):
				# Символ пустой строки нужен иногда, чтобы имитировать абзацы
				parsed_piece = {
					"type": "plain",
					"text": piece_text
				}
				parsed_tag.append(parsed_piece)
			else:
				if piece.name == 'a':
					parsed_piece = {
						"type": "a",
						"href": piece["href"],
						"text": piece_text
					}

				if piece.name == 'b' or piece.name == 'strong':
					parsed_piece = {
						"type": "plain",
						"bold": "true",
						"text": piece_text
					}

				if piece.name == 'i' or piece.name == 'em':
					parsed_piece = {
						"type": "plain",
						"cursive": "true",
						"text": piece_text
					}

				if piece.name in ('var', 'font'):
					parsed_piece = {
						"type": "plain",
						"text": piece_text
					}

				if piece.name == 'iframe':
					continue
				if piece.name == 'script':
					continue

				if piece.name == 'span':
					parsed_tag += self.__parse_tags(piece)
				elif piece.name == 'article':
					parsed_tag += self.__parse_tags(piece)
				elif piece.name == 'p':
					parsed_tag += self.__parse_tags(piece)
				else:
					parsed_tag.append(parsed_piece)
			
		return parsed_tag

	# def __squeeze_tags(self, tag):
	# 	squeezed_tags = ""

	# 	for piece in tag.children:
	# 		if piece.name == 'iframe' or piece.name == 'script':
	# 			continue
	# 		if piece.name == 'span':
	# 			squeezed_tags += self.__squeeze_tags(piece)
	# 		elif piece.name == 'article':
	# 			squeezed_tags += self.__squeeze_tags(piece)
	# 		elif piece.name == 'p':
	# 			squeezed_tags += self.__squeeze_tags(piece)
	# 		else:
	# 			squeezed_tags.append()

	# 	return squeezed_tags

	def get_last_news(self):
		news = copy.deepcopy(self.last_news)
		for i in range(len(news)):
			news[i]['time'] = self.__prettify_date(news[i]['time'])
		return news

	def drop_last_news(self):
		self.last_news = deque()

	def current_new(self):
		return self.__current_new

	def get_source(self):
		return self.source

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


if __name__ == "__main__":
	parser = Tatar_inform()
	parser.fix_last_new()
	print(parser.current_new())

	#parser.find_last_news()
	#print(parser.current_new())
	#print(parser._Tatar_inform__current_new)
	# print(parser.current_new())
	# print('-----------------------------------------------------')
	# print('-----------------------------------------------------')
	# for i in range(240):
	# 	parser.find_last_news()
	# 	if len(parser.get_last_news()) > 0:
	# 		print(parser.get_last_news())
	# 		print('-----------------------------------------------------')
	# 		parser.drop_last_news()
	# 	else:
	# 		print('havent got any {}'.format(datetime.now().strftime("%H:%M:%S")))
	# 		print()
	# 		print('-----------------------------------------------------')
	# 	time.sleep(30)