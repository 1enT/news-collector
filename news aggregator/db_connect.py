import psycopg2
import logging

from dotenv import load_dotenv
import os
load_dotenv()

db_password = os.environ.get('DB_PASSWORD')

class DatabaseProducer:
	def put(self, row):
		with psycopg2.connect(dbname="news_collector", user="postgres", password=db_password, host="localhost") as conn:
			with conn.cursor() as cursor:
				try:
					cursor.execute("LOCK TABLE awaiting_news IN ACCESS EXCLUSIVE MODE")
					cursor.execute("INSERT INTO last_news (source, time, title, lead, text, link) VALUES ('{}', '{}', '{}', '{}', '{}', '{}') RETURNING id".format(
								row['source'], 
								row['time'], 
								row['title'],
								row['lead'],
								row['text'],
								row['link']
							)
						)
					last_id = cursor.fetchone()[0]
					cursor.execute("INSERT INTO awaiting_news (last_news_id) VALUES ({})".format(last_id))
					conn.commit()
				except Exception as e:
					print(e)
					logging.critical(e)
					conn.rollback()

	def refresh(self):
		with psycopg2.connect(dbname="news_collector", user="postgres", password=db_password, host="localhost") as conn:
			with conn.cursor() as cursor:
				cursor.execute('TRUNCATE TABLE awaiting_news RESTART IDENTITY')
				conn.commit()

	def __total_refresh(self):
		with psycopg2.connect(dbname="news_collector", user="postgres", password=db_password, host="localhost") as conn:
			with conn.cursor() as cursor:
				cursor.execute('TRUNCATE TABLE last_news RESTART IDENTITY CASCADE')
				cursor.execute('TRUNCATE TABLE custom_news RESTART IDENTITY CASCADE')
				# Отдельно truncate остальные таблицы, чтобы рестартнуть id? 
				conn.commit()