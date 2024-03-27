import telebot
import psycopg2
import json
import prettytable as pt

from dotenv import load_dotenv
import os
load_dotenv()

db_password = os.environ.get('DB_PASSWORD')
token = os.environ.get('TELEGRAM_TOKEN')
proxy = os.environ.get('PROXY')
use_proxy = True if os.environ.get('USE_PROXY') == 'true' else False

bot = telebot.TeleBot(token)
if use_proxy:
	telebot.apihelper.proxy = {
				"http": proxy,
				"https": proxy
	}
conn = psycopg2.connect(dbname="news_collector", user="postgres", password=db_password, host="localhost")

allowed_usernames = ['s_enT']

@bot.message_handler(commands=['active_parsers'])
def active_parsers(message):
	with conn.cursor() as cursor:
		cursor.execute('SELECT type, name, status FROM parsers_status')
		parsers_status = cursor.fetchall()
		conn.commit()

		reply = ''
		for i in parsers_status:
			reply += f"{i[0]}	{i[1]}	{i[2]}\n"
		if reply == '':
			reply = 'Нет запущенных парсеров на данный момент'
		bot.reply_to(message, reply)

@bot.message_handler(commands=['awaiting_news'])
def awaiting_news(message):
	if message.from_user.username in allowed_usernames:
		text = ' '.join(message.text.split()[1:]).lower()
		reply = ''
		with conn.cursor() as cursor:
			match text:
				case 'count':
					cursor.execute('SELECT COUNT(id) FROM awaiting_news')
					reply = cursor.fetchall()[0][0]
				case '':
					max_count = 40
					cursor.execute('SELECT COUNT(id) FROM awaiting_news')
					count = int(cursor.fetchall()[0][0])
					cursor.execute("""
						WITH ater AS (
							SELECT b.id, source, time FROM awaiting_news a JOIN last_news b ON a.last_news_id = b.id LIMIT {}
						)
						SELECT * FROM ater
					""".format(max_count))
					table = pt.from_db_cursor(cursor)
					table = table.get_string()
					if count > max_count:
						table += '{}\n+ ещё {} новостей'.format('\n.......'*2, count - max_count)

					reply = f"<pre>{table}</pre>"
			if text.isdigit():
				cursor.execute("""
					WITH ater AS (
						SELECT b.id, source, time, title, lead, text, link FROM awaiting_news a JOIN last_news b ON a.last_news_id = b.id WHERE b.id = {}
					)
					SELECT to_json(ater) FROM ater
				""".format(text))
				t = cursor.fetchall()[0][0]
				for key in t:
					reply += "<b>{}</b>\n    {}\n\n".format(key, t[key])
			conn.commit()
			
		if reply == '':
			reply = 'Неправильный запрос'
		bot.reply_to(message, reply, parse_mode = "html", disable_web_page_preview = True)
	else:
		bot.reply_to(message, 'Нет доступа', parse_mode = "html", disable_web_page_preview = True)

@bot.message_handler(commands=['reload_news'])
def reload_news(message):
	if message.from_user.username in allowed_usernames:
		text = ' '.join(message.text.split()[1:]).lower()
		if text == 'root':
			with conn.cursor() as cursor:
				try:
					cursor.execute('TRUNCATE TABLE awaiting_news RESTART IDENTITY')
					conn.commit()
					bot.reply_to(message, "Таблица очищена", parse_mode = "html", disable_web_page_preview = True)
				except Exception as e:
					conn.rollback()
					bot.reply_to(message, f"Произошла ошибка при очистке таблицы\n<pre>{e}</pre>", parse_mode = "html", disable_web_page_preview = True)
		else:
			bot.reply_to(message, f"Неправильный запрос", parse_mode = "html", disable_web_page_preview = True)
	else:
		bot.reply_to(message, 'Нет доступа')

bot.infinity_polling()