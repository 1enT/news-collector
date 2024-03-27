import requests
from bs4 import BeautifulSoup
from collections import deque
import re
import json
import copy

from datetime import datetime, date
import locale
locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))

class Sovmo_gossov_prav:
	def __init__(self, url, url_to_files = "supportive files"):
		self.url_to_files = url_to_files
		self.url = url
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
		lead = very_last_one.find(attrs={"class": "list__text"}).p.string.replace('\xa0', '').strip()
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
			if self.__current_new['time'] < time:
				for each_new in one_day.find_all(attrs={"class": "list__item"}):
					title = each_new.find(attrs={"class": "list__title"}).a.string.replace('\xa0', '').strip()
					lead = each_new.find(attrs={"class": "list__text"}).p.string.replace('\xa0', '').strip()
					link = self.url + each_new.find(attrs={"class": "list__title"}).a.get('href')
					if title == self.__current_new['title']:
						break
					self.last_news.append({"source": self.url, "time": time, "title": title, "lead": lead, "text": "", "link": link, "img_url": None})
			else:
				break

		if len(self.last_news) > 0:
			self.__current_new = self.last_news[0]

	def get_last_news(self):
		news = copy.deepcopy(self.last_news)
		for i in range(len(news)):
			news[i]['time'] = self.__prettify_date()
		return news

	def drop_last_news(self):
		self.last_news = deque()

	def current_new(self):
		return self.__current_new

	def __get_date(self, text):
		date = re.search(r"\d+ [а-яА-Я]+ \d{4}", text)[0].split()
		with open(f"{self.url_to_files}/russian_months.json", encoding='utf8') as file:
			months = json.loads(file.read())
			date = ' '.join([date[0], months[date[1]], date[2]])
		return datetime.strptime(date, "%d %B %Y")

	def __prettify_date(self):
		now = datetime.now().strftime('%Y-%m-%d %H:%M')
		return now


if __name__ == "__main__":
	parser = Sovmo_gossov_prav("https://prav.tatarstan.ru")
	parser.fix_last_new()
	#parser.find_last_news()
	#print(parser.last_news)
	print(parser.current_new())