import requests
from bs4 import BeautifulSoup
from collections import deque

from datetime import datetime, date

class Tatmedia:
	def __init__(self, url = "", url_to_files = ""):
		self.__current_new = {"time": datetime.strptime("09:47", "%H:%M"), 
			   "title": "Татарстан вошел в топ-5 регионов России по качеству жизни в 2022 году",
			   "lead": "Первые семь позиций в рейтинге с 2021 года остались неизменными.",
			   "link": "http://mendeleevskyi.ru/news/obschestvo/tatarstan-vosel-v-top-5-regionov-rossii-po-kacestvu-zizni-v-2022-godu",
			   "img_url": "http://mendeleevskyi.ru/images/uploads/news/2023/2/13/d2ac40d1f9eebec35e9bb1e45e195fd5.jpg"}
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
		page = requests.get("https://tatmedia.ru/newscollector/news", stream = True, headers = self.__cookies)
		soup = BeautifulSoup(page.content, "html.parser")
		last_one = soup.find(attrs={"class", "tm-news"}).find(attrs={"class", "tm-news__item"})

		time = datetime.strptime(last_one.find(attrs={"class":"tm-news__time"}).string, "%H:%M")
		title = last_one.find(attrs={"class":"tm-news__title"}).string.replace('\xa0', '')
		lead = last_one.find(attrs={"class":"tm-news__overview"}).string.replace('\n', '').replace('\xa0', '').strip()
		link = last_one.find(attrs={"class":"tm-news__title"}).get('href')
		img_url = last_one.find('img')
		if img_url != None:
			img_url = img_url.get('src')

		self.__current_new = {"source": "tatmedia", "time": time, "title": title, "lead": lead, "link": link, "img_url": img_url}


	def find_last_news(self):
		page = requests.get("https://tatmedia.ru/newscollector/news", stream = True, headers = self.__cookies)
		soup = BeautifulSoup(page.content, "html.parser")
		list_of_news = soup.find(attrs={"class", "tm-news"}).find_all(attrs={"class", "tm-news__item"})

		for i, each_new in enumerate(list_of_news):
			time = datetime.strptime(each_new.find(attrs={"class":"tm-news__time"}).string, "%H:%M")
			if self.__current_new['time'] <= time:
				title = each_new.find(attrs={"class":"tm-news__title"}).string.replace('\xa0', '')
				lead = each_new.find(attrs={"class":"tm-news__overview"}).string.replace('\n', '').replace('\xa0', '').strip()
				link = each_new.find(attrs={"class":"tm-news__title"}).get('href')
				img_url = each_new.find('img')
				if img_url != None:
					img_url = img_url.get('src')
				if title == self.__current_new['title']:
					break
				self.last_news.append({"source": "tatmedia", "time": time, "title": title, "lead": lead, "link": link, "img_url": img_url})
			else:
				break
		if len(self.last_news) > 0:
			self.__current_new = self.last_news[0]

	def current_new(self):
		return self.__current_new


if __name__ == "__main__":
	parser = Tatmedia()
	#parser.fix_last_new()
	parser.find_last_news()
	print(parser.last_news)
	print()
	print(parser.current_new)