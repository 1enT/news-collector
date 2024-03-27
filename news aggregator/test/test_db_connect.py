import psycopg2

class DatabaseProducer:
	def __init__(self):
		self.conn = psycopg2.connect(dbname="news_collector", user="postgres", password="qwerty", host="localhost")
		self.cursor = self.conn.cursor()

	def put(self, row):
		self.cursor.execute("INSERT INTO last_news (source, time, title, lead, text, link) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(
					row['source'], 
					row['time'], 
					row['title'],
					' ' if row['lead'] == '' else row['lead'],
					row['text'],
					row['link']
				)
			)
		self.conn.commit()

	def refresh(self):
		self.cursor.execute('TRUNCATE TABLE last_news RESTART IDENTITY')
		self.conn.commit()