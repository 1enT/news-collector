# from strsimpy.levenshtein import Levenshtein

# levenshtein = Levenshtein()
# s1 = 'корпус'
# s2 = 'корень'
# print(levenshtein.distance(s1, s2))

import nltk
import get_data

text = get_data.get_text()
keyword = "глава муниципального района"
deviation = 8 # 5 by default

keyword_len = len(keyword.split())
for i in range(0, len(text) - keyword_len + 1):
	slice_of_text = text[i:i + keyword_len]
	slice_of_text = ' '.join(slice_of_text)
	slice_of_text = slice_of_text.lower()
	keyword = keyword.lower()
	dist = nltk.edit_distance(keyword, slice_of_text)
	if dist <= deviation:
		print(f"{keyword} | {slice_of_text} | {str(dist)}")