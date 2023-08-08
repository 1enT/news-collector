import json

with open('app/news.json', encoding="utf-8") as f:
	a = json.loads(f.read())
	print(a[1])