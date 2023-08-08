#from parsers.kzn import Kzn
from parsers.nabchelny import Nabchelny
from parsers.rais import Rais
from parsers.sovmo_gossov_prav import Sovmo_gossov_prav
from parsers.tatar_inform import Tatar_inform
#from parsers.tatmedia import Tatmedia

#from bot import Bot
from db_connect import DatabaseProducer

from collections import deque
import asyncio
import time

import logging

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
			db.put(cls.deque.pop())
			#cls.deque.pop()
		print("reached __got_news | deque len", len(cls.deque))

	def last_news(self):
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
			
			self.__put_in_deque(self.parser.get_last_news())
			self.parser.drop_last_news()
			self.__got_news_in_deque()
				
			print()
			print(f"current_new {self.parser.current_new()}")
			print('----------------------------------------------')
			print('----------------------------------------------')


db = DatabaseProducer()
#bot = Bot()
print()
print()
#tatmedia = Parser(Tatmedia)
tatar_inform = Parser(Tatar_inform, url_to_files = "parsers/supportive files")
nabchelny = Parser(Nabchelny, url_to_files = "parsers/supportive files")
#kzn = Parser(Kzn)
sovmo = Parser(Sovmo_gossov_prav, url = "https://sovmo.tatarstan.ru", url_to_files = "parsers/supportive files")
gossov = Parser(Sovmo_gossov_prav, url = "https://gossov.tatarstan.ru", url_to_files = "parsers/supportive files")
prav = Parser(Sovmo_gossov_prav, url = "https://prav.tatarstan.ru", url_to_files = "parsers/supportive files")
rais = Parser(Rais)
print('--------------------------------------------------------------------\n--------------------------------------------------------------------')


def main():
	#tatmedia.last_news()
	tatar_inform.last_news()
	nabchelny.last_news()
	#kzn.last_news()
	sovmo.last_news()
	gossov.last_news()
	prav.last_news()
	rais.last_news()

logging.basicConfig(level=logging.INFO, filename="logs.log", format="%(asctime)s %(levelname)s %(message)s")
logging.info("APP RUN-------------------------------------------------------------")
for i in range(240):
	try:
		main()
		logging.info("Done")
		time.sleep(30)
	except Exception as e:
		logging.critical("Exception", exc_info=True)