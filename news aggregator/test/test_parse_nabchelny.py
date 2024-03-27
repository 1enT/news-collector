import requests
from bs4 import BeautifulSoup
import bs4
import json

from test_db_connect import DatabaseProducer

class Test_class:
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

	def parse_news_body(self, url):
		page = requests.get(url, stream = True, headers = self.__cookies)
		soup = BeautifulSoup(page.content, "html.parser")
		content = soup.find(attrs={"class": "news_story"})
		content_text = [i for i in content.children if i != '\n' and i != ' ']

		parsed_content = []
		#print(content_text)
		for item in content_text:
			# img = item.find('img')
			# if img != -1 and img is not None:
			# 	img_src = img['src']
			# 	parsed_tag = {
			# 			"type": "img",
			# 			"src": "https://nabchelny.ru{}".format(img_src),
			# 			"children": [{"text": ""}]
			# 		}
			# 	parsed_content.append(parsed_tag)
			#if item.text.replace('\n', '').replace('\r', '') != '':
			if isinstance(item, bs4.element.NavigableString):
				parsed_content.append({
					"type": "plain",
					"text": item
				})
			elif len(item.contents) > 0:
				# parsed_tag = {
				# 			"type": "plain",
				# 			"text": item.text.replace('\n', '').replace('\r', '')
				# 		}
				#print(item)
				parsed_tag = self.__recursive_children_search(item)
				#parsed_content.append(parsed_tag)
				list(map(lambda x: parsed_content.append(x), parsed_tag))

		return parsed_content

	def __recursive_children_search(self, tag):
		parsed_tag = []
		
		for piece in tag.children:
			if piece.name == 'br' or piece == '\n':
				continue
			
			# if isinstance(piece, bs4.element.NavigableString) or piece.find('p') is None:
			if not isinstance(piece, bs4.element.NavigableString):
				is_only_nav_in_tag = self.__if_only_nav_string_in_tag(piece)
				is_only_img_in_tag = self.__if_only_img_in_tag(piece)

			if isinstance(piece, bs4.element.NavigableString) or is_only_nav_in_tag and not is_only_img_in_tag:
				text = piece.text.replace('\n', ' ')
				if text != ' ' and text != '':
					parsed_piece = [{
						"type": "plain",
						"text": text
					}]
				else:
					parsed_piece = []

			elif piece.name == 'img' or is_only_img_in_tag and not is_only_nav_in_tag:# or piece.find('img') is not None and piece.find('p') is None:
				if piece.name == 'img':
					all_imgs = [piece]
				else:
					all_imgs = piece.find_all('img')
				parsed_piece = []
				for img in all_imgs:
					parsed_piece.append({
							"type": "img",
							"src": "http://nabchelny.ru" + img['src'],
							"children": [{"text": ""}]
						})

			elif piece.name == "p" and piece.find('p') is not None:
				parsed_piece = self.__recursive_children_search(piece)

			# elif piece.name == "span":
			# 	# print(4)
			# 	# print(piece)
			# 	parsed_piece = self.__recursive_children_search(piece)

			# elif piece.name == "div":
			# 	# print(4)
			# 	# print(piece)
			# 	parsed_piece = self.__recursive_children_search(piece)
			else:
				parsed_piece = self.__recursive_children_search(piece)

			list(map(lambda x: parsed_tag.append(x), parsed_piece))
			del parsed_piece
		

		return parsed_tag

	def __if_only_nav_string_in_tag(self, tag):
		if tag.name == 'img':
			return False
		for i in tag.descendants:
			if i.name == 'img':
				return False
		return True

	def __if_only_img_in_tag(self, tag):
		if len(tag.contents) == 0 and tag.name != 'img':
			return False
		for i in tag.descendants:
			if isinstance(i, bs4.element.NavigableString):
				return False
		return True

tatar = Test_class()
text = tatar.parse_news_body("https://nabchelny.ru/news/52582")
text = json.dumps(text, ensure_ascii=False).encode('utf8').decode()
print(text)
news = {"source": "Наб. челны", "time": "2000-1-11 18:18", "title": "Какой-то заголовок", "lead": "", "text": text, "link": "http"}
# db = DatabaseProducer()
# db.put(news)