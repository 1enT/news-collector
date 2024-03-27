# from strsimpy.levenshtein import Levenshtein

# levenshtein = Levenshtein()
# s1 = 'корпус'
# s2 = 'корень'
# print(levenshtein.distance(s1, s2))

import nltk
import get_data

# s1 = 'Алексей Песошин'
# s2 = 'Алексею Песошину'
# print(nltk.edit_distance(s1, s2))

text = get_data.get_text()
#keywords = ['муниципалитет ', 'район ', 'самообложение ', 'гранты', 'грант ', 'муниципальная практика ', 'муниципальный служащий', 'местное самоуправление', 'национальный проект', 'федеральная программа', 'капитальный ремонт', 'демография', 'органы местного самоуправления', 'глава района', 'глава муниципалитета', 'глава поселения', 'прием граждан', 'землячество', 'тос', 'стос', 'стратегическое развитие', 'национальные традиции', 'развитие туризма', 'качественные и безопасные дороги', 'местные власти', 'сельчане ']
keywords = get_data.get_keywords()
deviation = 10 # 5 by default

for keyword in keywords:
	keyword_len = len(keyword.split())
	for i in range(0, len(text) - keyword_len + 1):
		slice_of_text = text[i:i + keyword_len]
		slice_of_text = ' '.join(slice_of_text)
		slice_of_text = slice_of_text.lower()
		keyword = keyword.lower()
		dist = nltk.edit_distance(keyword, slice_of_text)
	# 	if dist <= deviation:
	# 		print(f"{keyword} | {slice_of_text} | {str(dist)}")
	# print()