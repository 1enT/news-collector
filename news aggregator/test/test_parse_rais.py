import requests
from bs4 import BeautifulSoup
import bs4
import json

from test_db_connect import DatabaseProducer

class Rais:
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

	def parse_news_body(self, new):
		page = requests.get("https://rais.tatarstan.ru/index.htm/news?format=json&limit=15&page=1", stream = True, headers = self.__cookies)
		data = json.loads(page.content)
		new = data['items'][0]
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

rais = Rais()
text = rais.parse_news_body("https://www.tatar-inform.ru/news/ceburaska-5916088")
text = json.dumps(text, ensure_ascii=False).encode('utf8').decode()
print(text)
news = {"source": "rais", "time": "2000-1-11 18:18", "title": "Какой-то заголовок", "lead": "", "text": text, "link": "http"}