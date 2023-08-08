from flask import Flask, request, jsonify
import json
import time
import psycopg2
from datetime import datetime

app = Flask(__name__)

@app.route('/')
@app.route('/api')
@app.route('/socket.io')
def index():
	# with open('app/news.json', encoding="utf-8") as f:
	# 	a = f.read()
	# 	return a

	# cursor.execute('''
	# 	DELETE FROM
	# 	    last_news
	# 	USING (
	# 	    SELECT * FROM last_news
	# 	) q
	# 	WHERE last_news.id = q.id RETURNING last_news.*;
	# ''')
	#conn.commit()

	conn = psycopg2.connect(dbname="news_collector", user="postgres", password="qwerty", host="localhost")
	cursor = conn.cursor()

	cursor.execute('select json_agg(to_json(last_news)) from last_news')
	news = cursor.fetchall()
	conn.close()

	with open('logs.txt', 'a') as file:
		file.write(datetime.now().strftime('%Y-%m-%d %H:%M') + '\n')
		file.write(str(news))
		file.write('\n\n\n\n')
	return news[0][0] if news[0][0] is not None else []
	
@app.route('/dispose')
def dispose():
	conn = psycopg2.connect(dbname="news_collector", user="postgres", password="qwerty", host="localhost")
	cursor = conn.cursor()

	cursor.execute('delete from last_news where id=' + request.args['num'])
	conn.commit()
	conn.close()
	return request.args['num']

@app.route('/test')
def test():
	with open('app/news 2.json', encoding="utf-8") as f:
		a = f.read()
		return a