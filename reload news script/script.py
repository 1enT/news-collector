import psycopg2
import time
import threading
from datetime import datetime

from dotenv import load_dotenv
import os
load_dotenv()

db_password = os.environ.get('DB_PASSWORD')

def start():
	while True:
		with psycopg2.connect(dbname="news_collector", user="postgres", password=db_password, host="localhost") as conn:
			with conn.cursor() as cursor:
				try:
					cursor.execute('TRUNCATE TABLE awaiting_news RESTART IDENTITY')
					conn.commit()
					print(f'{datetime.now()} Truncated')
				except Exception as e:
					conn.rollback()
					raise Exception(e)
		time.sleep(86400)

today = datetime.now()
tommorow = datetime(today.year, today.month, today.day+1)
delay = int((tommorow - today).total_seconds())

threading.Timer(delay, start).start()