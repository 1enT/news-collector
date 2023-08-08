from db_connect import DatabaseProducer
import psycopg2

query = {
	'source': 'Татар-информ', 
	'time': '2023-8-2 0:26',
	'title': '«Даже кошка безбашенная»: командир спецназа «Ахмат» показал быт бойцов и их любимицу', 
	'lead': '', 
	'text': '''{
		children: [
			{
				type: "img",
				src: "https://kzn.ru/upload/iblock/e99/e99dea17859c35436be3865bc98ae84f.jpg"
			},
			{
				type: "p",
				text: "(Город Казань KZN.RU, 3 марта). В 2022 году специалисты Управления Роспотребнадзора по РТ изъяли из оборота 939 партий некачественных и опасных продуктов и сырья общим весом 17,5 тонны. Для сравнения, в 2021 году было изъято 1517 партий весом 40,4 тонны."
			},
			{
				type: "p",
				text: "Доля партий забракованных продуктов отечественного производства составила 93,6%, импортируемых - 6,4%. Больше всего изъято плодов и овощей - 232 партии, молока и молочной продукции - 66 партий, мукомольно-крупяных изделий - 61 партия, птицы, яиц и продуктов их переработки - 56 партий, а также мяса и мясной продукции - 53 партии. Забраковано 6333 кг плодоовощной продукции, 5234 кг мяса и мясной продукции, включая птицу, яйца и продукты их переработки, 2460 кг прочих пищевых продуктов и 2180 кг мукомольно-крупяных изделий."
			},
			{
				type: "p",
				text: "Продукцию изымали из оборота в основном из-за отсутствия маркировки, нарушения условий хранения, истечения срока годности, несоответствия продукции по результатам лабораторных испытаний, отсутствия товаросопроводительных документов, подтверждающих качество и безопасность продукции."
			},
			{
				type: "p",
				text: "Информация об изъятой продукции с указанием причин опубликована на портале Роспотребнадзора в разделе «Продукция, не соответствующая обязательным требованиям». Выявление и пресечение оборота некачественной и опасной продукции в республике продолжается, сообщает пресс-служба ведомства."
			}
		]
	}'''.replace('\n', ''),
	'link': 'https://www.tatar-inform.ru/news/daze-koska-bezbasennaya-komandir-specnaza-axmat-pokazal-byt-boicov-i-ix-lyubimicu-5914849', 
	'img_url': None
}

db = DatabaseProducer()
db.refresh()
db.put(query)
# db.put(query)
# db.put(query)

# conn = psycopg2.connect(dbname="news_collector", user="postgres", password="qwerty", host="localhost")
# cursor = conn.cursor()

# cursor.execute('''
# 	WITH GOTTEN_NEWS AS (SELECT json_agg(to_json(last_news)) FROM last_news)
# 	DELETE FROM
# 	    last_news
# 	USING (
# 	    SELECT * FROM last_news
# 	) q
# 	WHERE last_news.id = q.id;
# 	SELECT json_agg(to_json(last_news)) FROM last_news;
# ''')
# conn.commit()

# cursor.execute('select json_agg(to_json(last_news)) from last_news')
# news = cursor.fetchall()
# print(news[0][0])