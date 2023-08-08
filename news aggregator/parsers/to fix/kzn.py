import requests
from bs4 import BeautifulSoup
from collections import deque
import re

from datetime import datetime, date

class Kzn:
	def __init__(self, url = "", url_to_files=""):
		self.__current_new = {"time": datetime.strptime("12.02.2023, 10:37", "%d.%m.%Y, %H:%M"), 
			   "title": "Цифровая Казань: какие полезные сервисы есть у горожан",
			   "lead": "Как решить вопросы ЖКХ, оплатить парковку или продлить срок возврата книги в библиотеку с помощью приложений – в материале KZN.RU.",
			   "link": "https://kzn.ru/meriya/press-tsentr/novosti/tsifrovaya-kazan-kakie-poleznye-servisy-est-u-gorozhan/",
			   "img_url": "https://kzn.ru/meriya/press-tsentr/novosti/tsifrovaya-kazan-kakie-poleznye-servisy-est-u-gorozhan/"}
		self.last_news = deque()
		self.__cookies = {
								"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
								"Accept-Encoding": "gzip, deflate, br",
								"Accept-Language": "ru-RU,ru;q=0.7",
								"Cache-Control": "max-age=0",
								"Connection": "keep-alive",
								"Cookie": "LANG=ru; BITRIX_SM_GUEST_ID=5570555; BITRIX_SM_LAST_ADV=7; session-cookie=17434ee7a0b5703ec848e955beb261f5c992f4df352b3fd888e80a64f826e0336bce8ec7cf0c6afe48fd6252fdde58b2; PHPSESSID=7567ea0da9f5c355ba05dabd6822b9f2; BITRIX_SM_LAST_VISIT=13.02.2023+11%3A13%3A50",
								"Host": "kzn.ru",
								"Sec-Fetch-Dest": "document",
								"Sec-Fetch-Mode": "navigate",
								"Sec-Fetch-Site": "none",
								"Sec-Fetch-User": "?1",
								"Sec-GPC": "1",
								"Upgrade-Insecure-Requests": "1",
								"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
								}

	def fix_last_new(self):
		page = requests.get("https://kzn.ru/meriya/press-tsentr/novosti", stream = True, headers = self.__cookies)
		soup = BeautifulSoup(page.content, "html.parser")
		last_one = soup.find(attrs={"class", "news-lists-bl"}).find(attrs={"class", "news-lists__item"})

		time = datetime.strptime(last_one.find(attrs={"class":"news-lists__date"}).string, "%d.%m.%Y, %H:%M")
		title = last_one.find(attrs={"class":"news-lists__caption"}).a.string
		lead = last_one.find(attrs={"class":"news-lists__text"}).string
		link = "https://kzn.ru" + last_one.find(attrs={"class":"news-lists__caption"}).a.get('href')
		img_url = last_one.find('img')
		if img_url != None:
			img_url = "https://kzn.ru" + img_url.get('src')
		self.__current_new = {"source": "kzn", "time": time, "title": title, "lead": lead, "link": link, "img_url": img_url}

	def find_last_news(self):
		# https://kzn.ru/meriya/press-tsentr/novosti/?ALL_FIELDS=%D1%81%D0%BB%D0%BE%D0%B2%D0%BE&DATE_FROM=&DATE_TO=&PROPERTY_REF_NR=-1&submit=Y
		page = requests.get("https://kzn.ru/meriya/press-tsentr/novosti", stream = True, headers = self.__cookies)
		soup = BeautifulSoup(page.content, "html.parser")
		list_of_news = soup.find(attrs={"class", "news-lists-bl"}).find_all(attrs={"class", "news-lists__item"})

		for each_new in list_of_news:
			time = datetime.strptime(each_new.find(attrs={"class":"news-lists__date"}).string, "%d.%m.%Y, %H:%M")
			if self.__current_new['time'] <= time:
				title = each_new.find(attrs={"class":"news-lists__caption"}).a.string
				lead = each_new.find(attrs={"class":"news-lists__text"}).string
				link = "https://kzn.ru" + each_new.find(attrs={"class":"news-lists__caption"}).a.get('href')
				img_url = each_new.find('img')
				if img_url != None:
					img_url = "https://kzn.ru" + img_url.get('src')
				if title == self.__current_new['title']:
					break
				self.last_news.append({"source": "kzn", "time": time, "title": title, "lead": lead, "link": link, "img_url": img_url})
			else:
				break
		if len(self.last_news) > 0:
			self.__current_new = self.last_news[0]

	def current_new(self):
		return self.__current_new

if __name__ == "__main__":
	parser = Kzn()
	#parser.fix_last_new()
	parser.find_last_news()
	print(parser.last_news)
	#print(parser._Kzn__current_new)