from parsers.tatarstan_domain.tatarstan import Tatarstan
from parsers.others.rais import Rais
from parsers.others.tatar_inform import Tatar_inform

from db_connect import DatabaseProducer
from searcher import Searcher

from collections import deque
import asyncio
import time
import json

import logging
from datetime import datetime

class Parser:
	def __init__(self, parser, url = "", source = "", is_tat_domain = False):
		self.source = source
		self.url = url
		self.is_tat_domain = is_tat_domain
		if is_tat_domain:
			self.parser = parser(url = url, source = self.source)
		else:
			self.parser = parser()
		self.parser.set_sup_files_url(url_to_sup_files)
		self.parser.fix_last_new()
		self.__init_deque()
		print('--------------------')
		print(self.parser)
		print(self.source)
		print(self.parser.current_new())
		print('--------------------')
		logging.info(f"--------------------\n{self.parser}\n{self.source}\n{self.parser.current_new()}\n--------------------")

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
			news = cls.deque.popleft() ####################################
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

	def last_news(self):
		self.parser.find_last_news()
		if len(self.parser.get_last_news()) > 0:
			print('----------------------------------------------')
			print('----------------------------------------------')
			print(self.parser)
			print(self.parser.get_last_news())
			print()
			logging.info(self.parser.source)
			logging.info(self.parser.get_last_news())
			
			self.__put_in_deque(self.parser.get_last_news())
			self.parser.drop_last_news()
			self.__got_news_in_deque()
				
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
	def clear_deque(cls):
		cls.deque = deque()

	def test_parse(self):
		cur_new = self.parser.current_new()
		return f"{self.source}\n{cur_new['link']}\n{self.parser.test_parse(cur_new['link'])}"

logging.basicConfig(level=logging.INFO, filename="logs_test.log", encoding="utf-8", format="%(asctime)s %(levelname)s %(message)s")
logging.info("APP RUN-------------------------------------------------------------")

url_to_sup_files = "parsers/supportive files"
db = DatabaseProducer()
searcher = Searcher()
list_parsers = {
	"Татар-информ": Parser(Tatar_inform, source="Татар-информ"),
	"Раис": Parser(Rais, source="Раис")
}
with open('parsers/tatarstan_domain/others.txt', 'r', encoding="utf8") as file:
	lines = file.read().splitlines()
	for line in lines:
		line = line.split('#')
		url = line[0].strip()
		source = line[1].strip()
		list_parsers[source] = Parser(Tatarstan, url = url, source = source, is_tat_domain = True)
with open('parsers/tatarstan_domain/ministry_list.txt', 'r', encoding="utf8") as file:
	lines = file.read().splitlines()
	for line in lines:
		line = line.split('#')
		url = line[0].strip()
		source = line[1].strip()
		#print(line)
		list_parsers[source] = Parser(Tatarstan, url = url, source = source, is_tat_domain = True)
with open('parsers/tatarstan_domain/municipality_list.txt', 'r', encoding="utf8") as file:
	lines = file.read().splitlines()
	for line in lines:
		line = line.split('#')
		url = line[0].strip()
		source = line[1].strip()
		list_parsers[source] = Parser(Tatarstan, url = url, source = source, is_tat_domain = True)
print('--------------------------------------------------------------------\n--------------------------------------------------------------------')


corrupted_parsers = {}
while True:
	time.sleep(60)
	for key in list(list_parsers):
		try:
			list_parsers[key].last_news()
		except Exception as e:
			logging.critical(f"{list_parsers[key].source}")
			logging.critical(f"Last news {list_parsers[key].parser.get_last_news()}")
			logging.critical("Exception", exc_info=True)
			Parser.clear_deque()
			list_parsers[key].parser.fix_last_new()
			# corrupted_parsers[key] = list_parsers[key]
			# del list_parsers[key]
	logging.info(f"Done {len(corrupted_parsers)}")