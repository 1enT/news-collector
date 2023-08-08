from parse import Parse
from bot import Bot
import time
import pprint

bot = Bot()
#parser_sovmo = Parse("https://sovmo.tatarstan.ru")
#parser_gossov = Parse("https://gossov.tatarstan.ru")
#parser_prav = Parse("https://prav.tatarstan.ru")
parser_rais = Parse("https://rais.tatarstan.ru", pres=True)

# parser_rais.get_image()
# for per_new in parser_rais.all_day_news:
# 	bot.send_post(per_new)
# exit()
sovmo_news_now = parser_sovmo.all_day_news()
gossov_news_now = parser_gossov.all_day_news()
prav_news_now = parser_prav.all_day_news()
rais_news_now = parser_rais.all_day_news()

for i in range(1000):
	time.sleep(5)
	parser_sovmo.manual_parse()
	parser_gossov.manual_parse()
	parser_prav.manual_parse()
	parser_rais.manual_parse()

	sovmo_news_later = parser_sovmo.all_day_news()
	gossov_news_later = parser_gossov.all_day_news()
	prav_news_later = parser_prav.all_day_news()
	rais_news_later = parser_rais.all_day_news()

	total_stock = [[sovmo_news_now, sovmo_news_later], [gossov_news_now, gossov_news_later], [prav_news_now, prav_news_later], [rais_news_now, rais_news_later]]
	for i, each_stock in enumerate(total_stock):
		if each_stock[0] != each_stock[1]:
			for each in each_stock[0]:
				each_stock[1].pop(each_stock[1].index(each))
			for each in each_stock[1]:
				bot.send_post(each)
			current_stock_of_news = next_stock_of_news
			total_stock[i][0] = total_stock[i][1]