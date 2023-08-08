from parsers.kzn import Kzn
from parsers.nabchelny import Nabchelny
from parsers.rais import Rais
from parsers.sovmo_gossov_prav import Sovmo_gossov_prav
from parsers.tatar_inform import Tatar_inform
from parsers.tatmedia import Tatmedia
from bot import Bot

from collections import deque
import asyncio
import time

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
	async def __got_news_in_deque(cls):
		async with deque_lock:
			print('passed lock')
			# print("reached second WITH")
			while len(cls.deque) > 0:
				#bot.send_post(cls.deque.pop())
				cls.deque.pop()
			# print("ended second WITH | deque len", len(cls.deque))

	async def last_news(self):
		# print('---------------------------------------------------------------')
		# print('---------------------------------------------------------------')
		# print(self.parser)
		# print(f"last_news {self.parser.last_news}")
		# print()
		# print(f"current_new {self.parser.current_new()}")
		self.parser.find_last_news()
		if len(self.parser.last_news) > 0:
			print('----------------------------------------------')
			print('----------------------------------------------')
			print(self.parser)
			print(self.parser.last_news)
			print()
			async with parser_lock:
				# print("reached first WITH")
				self.__put_in_deque(self.parser.last_news)
				self.parser.last_news = deque()
				await self.__got_news_in_deque()
				print("ended first WITH")
			print()
			print(f"current_new {self.parser.current_new()}")
			print('----------------------------------------------')
			print('----------------------------------------------')


bot = Bot()
print()
print()
#tatmedia = Parser(Tatmedia)
tatar_inform = Parser(Tatar_inform, url_to_files = "parsers/supportive files")
#nabchelny = Parser(Nabchelny, url_to_files = "parsers/supportive files")
#kzn = Parser(Kzn)
#sovmo = Parser(Sovmo_gossov_prav, url = "https://sovmo.tatarstan.ru", url_to_files = "parsers/supportive files")
#gossov = Parser(Sovmo_gossov_prav, url = "https://gossov.tatarstan.ru", url_to_files = "parsers/supportive files")
#prav = Parser(Sovmo_gossov_prav, url = "https://prav.tatarstan.ru", url_to_files = "parsers/supportive files")
#rais = Parser(Rais)
print('--------------------------------------------------------------------\n--------------------------------------------------------------------')
parser_lock = asyncio.Lock()
deque_lock = asyncio.Lock()
async def main():
	#task1 = asyncio.create_task(tatmedia.last_news())
	task2 = asyncio.create_task(tatar_inform.last_news())
	#task3 = asyncio.create_task(nabchelny.last_news())
	#task4 = asyncio.create_task(kzn.last_news())
	#task5 = asyncio.create_task(sovmo.last_news())
	#task6 = asyncio.create_task(gossov.last_news())
	#task7 = asyncio.create_task(prav.last_news())
	#task8 = asyncio.create_task(rais.last_news())

	#await task1
	await task2
	#await task3
	#await task4
	#await task5
	#await task6
	#await task7
	#await task8

for i in range(120):
	asyncio.run(main())
	time.sleep(30)