import requests
from bs4 import BeautifulSoup
import bs4
import json
import re

from test_db_connect import DatabaseProducer

class Tatar_inform:
	def __init__(self):
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
					#print(j)
					if j == 0:
						parsed_content[i]['children'][j]['text'] = parsed_content[i]['children'][j]['text'].lstrip()
					if j == len(parsed_content[i]['children'])-1:
						parsed_content[i]['children'][j]['text'] = parsed_content[i]['children'][j]['text'].rstrip()
					piece = parsed_content[i]['children'][j]
					#print(i, j, piece)
					
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


					# print(i, j, piece)
					# print()
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
			if isinstance(piece, bs4.element.NavigableString):
				# Символ пустой строки нужен иногда, чтобы имитировать абзацы
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

				if piece.name == 'u':
					parsed_piece = {
						"type": "plain",
						"underline": "true",
						"text": piece.text
					}

				if piece.name in ('var', 'font'):
					parsed_piece = {
						"type": "plain",
						"text": piece.text
					}

				if piece.name == 'iframe':
					continue
				if piece.name == 'script':
					continue
				if piece.name == 'br':
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

tatar = Tatar_inform()
url = "https://www.tatar-inform.ru/news/predpriyatie-v-kazani-vyplatilo-bolee-2-mln-rublei-dolgov-po-zarplate-5939942"
text = tatar._Tatar_inform__parse_news_body(url)
text = json.dumps(text, ensure_ascii=False).encode('utf8').decode()
print(text)
news = {"source": "tatar-inform", "time": "2000-1-11 18:18", "title": "Какой-то заголовок", "lead": "", "text": text, "link": "http"}
# db = DatabaseProducer()
# db.put(news)