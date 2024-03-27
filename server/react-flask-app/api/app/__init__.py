from flask import Flask, redirect, url_for, request, jsonify, Response, make_response
from werkzeug.exceptions import HTTPException

import json
import requests
import psycopg2
from datetime import datetime
import logging
import telebot
from telebot.apihelper import ApiTelegramException
import traceback

from dotenv import load_dotenv
import os
load_dotenv()

db_password = os.environ.get('DB_PASSWORD')
token = os.environ.get('TELEGRAM_TOKEN')
proxy = os.environ.get('PROXY')
use_proxy = True if os.environ.get('USE_PROXY') == 'true' else False
channel_id = os.environ.get('CHANNEL_ID')

bot = telebot.TeleBot(token)
if use_proxy:
	telebot.apihelper.proxy = {
				"http": proxy,
				"https": proxy
	}

app = Flask(__name__)


@app.route('/test_post', methods = ['POST'])
def test_post():
	data = json.loads(request.data)
	print(data)
	return ''


@app.route('/')
@app.route('/api')
def index():
	gotten_news = request.args['gotten_news'].split('.')
	
	if gotten_news == ['']:
		gotten_news = ['-1']
	gotten_news = f"[{', '.join(gotten_news)}]"
	data = []

	with psycopg2.connect(dbname="news_collector", user="postgres", password=db_password, host="localhost") as conn:
		with conn.cursor() as cursor:
			cursor.execute("""
				WITH joined_table AS ( 
					SELECT last_news.id, source, time, title, lead, text, link FROM last_news JOIN awaiting_news ON last_news.id = awaiting_news.last_news_id
				), full_joined_table AS (
					SELECT joined_table.id id_table, x.id id_client, source, time, title, lead, text, link FROM joined_table FULL JOIN unnest(ARRAY{0}) x(id) ON joined_table.id = x.id
				), ater AS (
					SELECT id_table, id_client, source, time, title, lead, text, link, CASE
					WHEN id_client IS NULL THEN 'add'
					WHEN id_table IS NULL THEN 'delete'
					END "to_do"
					FROM full_joined_table WHERE id_client IS NULL OR (id_table IS NULL AND id_client != -1)
				)
				SELECT to_json(ater) FROM ater

			""".format(gotten_news)) # to_json json_agg
			data = cursor.fetchall()
			conn.commit()

	response = []
	for elem in data:
		elem = elem[0]
		on_delete = True if elem['to_do'] == 'delete' else False
		obj = {
			'id': elem['id_table'] if not on_delete else elem['id_client'],
			'to_do': elem['to_do']
		}
		if not on_delete:
			obj['content'] = {}
			obj['content']['id'] = obj['id']
			obj['content']['source'] = elem['source']
			obj['content']['time'] = elem['time']
			obj['content']['title'] = elem['title']
			obj['content']['lead'] = elem['lead']
			obj['content']['text'] = elem['text']
			obj['content']['link'] = elem['link']
		response.append(obj)
	return response
	

@app.route('/dispose')
def dispose():
	num = request.args['num']
	is_custom = request.args['is_custom']
	if is_custom == 'false':
		with psycopg2.connect(dbname="news_collector", user="postgres", password=db_password, host="localhost") as conn:
			with conn.cursor() as cursor:
				try:
					cursor.execute("LOCK TABLE awaiting_news IN ACCESS EXCLUSIVE MODE")
					cursor.execute("DELETE FROM awaiting_news WHERE last_news_id = {}".format(num))
					cursor.execute("INSERT INTO discarded_news (last_news_id) VALUES ({})".format(num))
					conn.commit()
				except Exception as e:
					conn.rollback()
					raise Exception(e)

	return request.args['num']


class PutPostIntoDb:
	def __init__(self):
		 pass

	@classmethod
	def execute(cls, is_custom, news_id, title, body, images = []):
		title = title.replace('"', "'")
		body = body.replace("'", '"')
		cls.conn = psycopg2.connect(dbname="news_collector", user="postgres", password=db_password, host="localhost")
		cls.cursor = cls.conn.cursor()
		try:
			if is_custom == 'false':
				cls.cursor.execute("LOCK TABLE awaiting_news IN ACCESS EXCLUSIVE MODE")
				cls.cursor.execute("DELETE FROM awaiting_news WHERE last_news_id = {}".format(news_id))
				cls.cursor.execute("INSERT INTO published_news (last_news_id, final_title, final_text) VALUES ({}, '{}', '{}') RETURNING id".format(news_id, title, body))
				if images != []:
					last_id = cls.cursor.fetchone()[0]
					images = "['{}']".format('\', \''.join(images))
					cls.cursor.execute("INSERT INTO published_news_img_src (published_news_id, src) SELECT {}, x.src FROM unnest(ARRAY{}) x(src)".format(last_id, images))
			else:
				cls.cursor.execute("INSERT INTO custom_news (title, text) VALUES ('{}', '{}') RETURNING id".format(title, body))
				if images != []:
					last_id = cls.cursor.fetchone()[0]
					images = "['{}']".format('\', \''.join(images))
					cls.cursor.execute("INSERT INTO custom_news_img_src (custom_news_id, src) SELECT {}, x.src FROM unnest(ARRAY{}) x(src)".format(last_id, images))
		except Exception as e:
			cls.rollback()
			raise Exception(e)

	@classmethod
	def rollback(cls):
		cls.conn.rollback()
		cls.cursor.close()
		cls.conn.close()

	@classmethod
	def commit(cls):
		cls.conn.commit()
		cls.cursor.close()
		cls.conn.close()



# def put_post_into_db(is_custom, news_id, title, body, images = []):
# 	title = title.replace('"', "'")
# 	body = body.replace("'", '"')
# 	with psycopg2.connect(dbname="news_collector", user="postgres", password=db_password, host="localhost") as conn:
# 		with conn.cursor() as cursor:
# 			try:
# 				if is_custom == 'false':
# 					cursor.execute("LOCK TABLE awaiting_news IN ACCESS EXCLUSIVE MODE")
# 					cursor.execute("DELETE FROM awaiting_news WHERE last_news_id = {}".format(news_id))
# 					cursor.execute("INSERT INTO published_news (last_news_id, final_title, final_text) VALUES ({}, '{}', '{}') RETURNING id".format(news_id, title, body))
# 					if images != []:
# 						last_id = cursor.fetchone()[0]
# 						images = "['{}']".format('\', \''.join(images))
# 						cursor.execute("INSERT INTO published_news_img_src (published_news_id, src) SELECT {}, x.src FROM unnest(ARRAY{}) x(src)".format(last_id, images))
# 				else:
# 					cursor.execute("INSERT INTO custom_news (title, text) VALUES ('{}', '{}') RETURNING id".format(title, body))
# 					if images != []:
# 						last_id = cursor.fetchone()[0]
# 						images = "['{}']".format('\', \''.join(images))
# 						cursor.execute("INSERT INTO custom_news_img_src (custom_news_id, src) SELECT {}, x.src FROM unnest(ARRAY{}) x(src)".format(last_id, images))
				
# 				conn.commit()
# 			except Exception as e:
# 				conn.rollback()
# 				raise Exception(e)


@app.route('/send_message', methods = ['POST'])
def send_message():
	news_id = request.form.get('news_id')
	is_custom = request.form.get('is_custom')
	message_title = request.form.get('message_title')
	message_body = request.form.get('message_body')
	message = f"{message_title}\n\n{message_body}"
	logs = message
	# put_post_into_db(news_id = news_id, title = message_title, body = message_body, is_custom = is_custom)
	PutPostIntoDb.execute(news_id = news_id, title = message_title, body = message_body, is_custom = is_custom)
	try:
		bot.send_message(channel_id, message, parse_mode = "markdownv2", disable_web_page_preview = True)
	except ApiTelegramException as e:
		log_telegram(logs = logs, on_error = 1, error_message = traceback.format_exc())
		PutPostIntoDb.rollback()
		return make_response('Telegram Error', 406)
	else:
		log_telegram(logs = logs, on_error = 0)
		PutPostIntoDb.commit()
		return make_response('It\'s fine', 200)


@app.route('/send_photo', methods = ['POST'])
def send_photo():
	news_id = request.form.get('news_id')
	is_custom = request.form.get('is_custom')
	caption_title = request.form.get('caption_title')
	caption_body = request.form.get('caption_body')
	caption = f"{caption_title}\n\n{caption_body}"
	photo_link = request.form.get('photo')
	local_image = request.files.to_dict().get('image0')
	images = []
	if photo_link is not None and photo_link != 'null':
		r = requests.get(photo_link)
		photo = r.content
		images.append(photo_link)
	if local_image is not None:
		photo = local_image
	logs = "{}\n\n{}".format(photo_link, caption)
	# put_post_into_db(news_id = news_id, title = caption_title, body = caption_body, images = images, is_custom = is_custom)
	PutPostIntoDb.execute(news_id = news_id, title = caption_title, body = caption_body, images = images, is_custom = is_custom)
	try:
		bot.send_photo(channel_id, photo, parse_mode = "markdownv2", caption = caption)
	except ApiTelegramException as e:
		log_telegram(logs = logs, on_error = 1, error_message = traceback.format_exc())
		PutPostIntoDb.rollback()
		return make_response('Telegram Error', 406)
	else:
		log_telegram(logs = logs, on_error = 0)
		PutPostIntoDb.commit()
		return make_response('It\'s fine', 200)


@app.route('/send_media_group', methods = ['POST'])
def send_media_group():
	news_id = request.form.get('news_id')
	is_custom = request.form.get('is_custom')
	caption_title = request.form.get('caption_title')
	caption_body = request.form.get('caption_body')
	caption = f"{caption_title}\n\n{caption_body}"
	media_link = json.loads(request.form.get('media'))
	media_local = list(request.files.to_dict().values())
	media = []
	logs = []
	images = []
	if media_link is not None and media_link != 'null':
		for i in range(len(media_link)):
			r = requests.get(media_link[i])
			media.append(telebot.types.InputMediaPhoto(media=r.content))
			logs.append(media_link[i])
			images.append(media_link[i])
	for img_local in media_local:
		media.append(telebot.types.InputMediaPhoto(media=img_local))
	media[0].caption = caption
	media[0].parse_mode = 'markdownv2'
	logs = "{}\n\n{}".format('\n'.join(logs), caption)
	# put_post_into_db(news_id = news_id, title = caption_title, body = caption_body, images = images, is_custom = is_custom)
	PutPostIntoDb.execute(news_id = news_id, title = caption_title, body = caption_body, images = images, is_custom = is_custom)
	try:
		bot.send_media_group(channel_id, media)
	except ApiTelegramException as e:
		log_telegram(logs = logs, on_error = 1, error_message = traceback.format_exc())
		PutPostIntoDb.rollback()
		return make_response('Telegram Error', 406)
	else:
		log_telegram(logs = logs, on_error = 0)
		PutPostIntoDb.commit()
		return make_response('It\'s fine', 200)
	

#@app.route('/log_telegram', methods = ['POST'])
def log_telegram(logs, on_error, error_message = ''):
	on_error = str(on_error)
	files = {'0': 'telegram_logs.log', 
			'1': 'telegram_error_logs.log'}
	with open(files[on_error], 'a', encoding="utf-8") as file:
		file.write(str(datetime.now()))
		file.write('\n')
		file.write(logs)
		file.write('\n\n')
		file.write(error_message + '\n')
		file.write(2*(70*'-'+'\n'))
	return ''


@app.route('/log_internal')
def log_internal():
	logs = request.args['logs']
	post_title = request.args['post_title']
	post_text = request.args['post_text']
	#try:
	with open('internal_error_logs.log', 'a', encoding="utf-8") as file:
		file.write(str(datetime.now()))
		file.write('\n')
		file.write(logs)
		file.write('\n\n' + (70*'-'+'\n'))
		file.write(post_title + '\n\n')
		file.write(post_text + '\n')
		file.write(2*(70*'-'+'\n'))
	# except Exception as e:
	# 	print(e)
	# 	print(logs)
	return ''


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name
    })
    response.content_type = "application/json"
    return response