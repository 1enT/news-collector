#from parsers.kzn import Kzn
#from parsers.nabchelny import Nabchelny
from parsers.rais import Rais
from parsers.sovmo_gossov_prav import Sovmo_gossov_prav
from parsers.tatar_inform import Tatar_inform
#from parsers.tatmedia import Tatmedia
	
#from bot import Bot
from db_connect import DatabaseProducer
from searcher import Searcher

from collections import deque
import asyncio
import time
import json

import logging
from datetime import datetime

class Parser:
	def __init__(self, parser, url = "", url_to_files = ""):
		self.parser = parser(url = url, url_to_files = url_to_files)
		#self.deque = deque()
		#self.deque.append(type(self.parser))
		self.parser.fix_last_new()
		self.__init_deque()
		print(self.parser)
		print(self.parser.current_new())
		print('--------------------')
		logging.info(f"{self.parser}\n{self.parser.source}\n{self.parser.current_new()}\n--------------------")

	@classmethod
	def __init_deque(cls):
		if not hasattr(cls, 'deque'):
			cls.deque = deque()

	@classmethod
	def __put_in_deque(cls, arr):
		cls.deque.extend(arr)

	@classmethod
	def __got_news_in_deque(cls):
		while len(cls.deque) > 0:
			#bot.send_post(cls.deque.pop())
			#db.put(cls.deque.pop())
			news = cls.deque.pop()
			raw_text = cls.__unpack_news_text(news)
			logging.info(raw_text)
			print(raw_text)
			raw_text = raw_text.split()
			logging.info(datetime.now().strftime('%H:%M:%S %f'))
			print(datetime.now().strftime('%H:%M:%S %f'))
			searcher.dump_text(raw_text)
			result = searcher.initiate()
			searcher.clear_cache()
			logging.info(datetime.now().strftime('%H:%M:%S %f'))
			print(datetime.now().strftime('%H:%M:%S %f'))

			if result:
				db.put(news)
		print("reached __got_news | deque len", len(cls.deque))

	def last_news(self):
		Добавить primary key к id
		Увеличить размер таблицы
		
		# print('---------------------------------------------------------------')
		# print('---------------------------------------------------------------')
		# print(self.parser)
		# print(f"last_news {self.parser.last_news}")
		# print()
		# print(f"current_new {self.parser.current_new()}")
		self.parser.find_last_news()
		if len(self.parser.get_last_news()) > 0:
			print('----------------------------------------------')
			print('----------------------------------------------')
			print(self.parser)
			print(self.parser.get_last_news())
			print()
			logging.info(self.parser.get_last_news())
			
			self.__put_in_deque(self.parser.get_last_news())
			self.parser.drop_last_news()
			self.__got_news_in_deque()
				
			# print()
			# print(f"current_new {self.parser.current_new()}")
			print('----------------------------------------------')
			print('----------------------------------------------')

	@classmethod
	def __unpack_news_text(cls, text):
		raw_text = []
		raw_tags = []
		text = json.loads(text['text'])
		for piece in text:
			if piece['type'] == 'p':
				for tags in piece['children']:
					raw_tags.append(tags['text'])
				raw_text.append(' '.join(raw_tags))
				raw_tags = []
		return '\n'.join(raw_text)

	@classmethod
	def refresh(cls):
		cls.deque = deque()

logging.basicConfig(level=logging.INFO, filename="logs.log", encoding="utf-8", format="%(asctime)s %(levelname)s %(message)s")
logging.info("APP RUN-------------------------------------------------------------")


db = DatabaseProducer()
searcher = Searcher()
#bot = Bot()
print()
print()
#tatmedia = Parser(Tatmedia)
tatar_inform = Parser(Tatar_inform, url_to_files = "parsers/supportive files")
#nabchelny = Parser(Nabchelny, url_to_files = "parsers/supportive files")
#kzn = Parser(Kzn)
sovmo = Parser(Sovmo_gossov_prav, url = "https://sovmo.tatarstan.ru", url_to_files = "parsers/supportive files")
gossov = Parser(Sovmo_gossov_prav, url = "https://gossov.tatarstan.ru", url_to_files = "parsers/supportive files")
prav = Parser(Sovmo_gossov_prav, url = "https://prav.tatarstan.ru", url_to_files = "parsers/supportive files")
rais = Parser(Rais)
print('--------------------------------------------------------------------\n--------------------------------------------------------------------')


def main():
	#tatmedia.last_news()
	tatar_inform.last_news()
	#nabchelny.last_news()
	#kzn.last_news()
	sovmo.last_news()
	gossov.last_news()
	prav.last_news()
	rais.last_news()

#for i in range(240):
while True:
	try:
		time.sleep(60)
		main()
		logging.info("Done")
	except Exception as e:
		logging.critical("Exception", exc_info=True)

		tatar_inform.refresh()
		#nabchelny.refresh()
		sovmo.refresh()
		gossov.refresh()
		prav.refresh()
		rais.refresh()
	# main()
	# time.sleep(30)