import nltk
from multiprocessing import Process
import math
import re
import get_data

import pymorphy3
import functools

# 2**10, 2**14, 2**16
@functools.lru_cache(maxsize=2**14)
def cached_dist(keyword, word_of_slice):
	keyword = keyword.lower()
	dist = nltk.edit_distance(keyword, word_of_slice)
	return dist

@functools.lru_cache(maxsize=2**10)
def cached_morph(cleared_word):
	return morph.parse(cleared_word)[0].tag.POS

def process_keywords_parts(num, text, words):
	for keyword in words:
		keyword_len = len(keyword.split())
		for i in range(0, len(text) - keyword_len + 1):
			slice_of_text = text[i:i + keyword_len]

			# slice_of_text = ' '.join(slice_of_text)
			# keyword = keyword.lower().strip()
			# dist = nltk.edit_distance(keyword, slice_of_text)

			keyword_splitted = keyword.lower().split()
			dist = 0
			for i in range(len(slice_of_text)):
				dist += cached_dist(keyword_splitted[i], slice_of_text[i])
			slice_of_text = ' '.join(slice_of_text)

			if dist/len(slice_of_text) <= deviation:
				print(f"{num} | {keyword} | {slice_of_text} | {str(dist)}")
	

def clear_text():
	cleared_text = []
	forbidden_types = {'NPRO', 'PRED', 'PREP', 'CONJ', 'PRCL', 'INTJ'}

	for word in text:
		word = word.lower()
		cleared_word = re.sub(r"[,.+–:;!?()\'\"@#№$%^&*\\/<>«»„“]", '', word)
		# morph_type = morph.parse(cleared_word)[0].tag.POS
		morph_type = cached_morph(cleared_word)
		#if morph_type != None and morph_type not in forbidden_types:
		if cleared_word != '' and morph_type not in forbidden_types:
			cleared_text.append(cleared_word)
	return cleared_text

################################
text = get_data.get_text('text 2.txt')
keywords = get_data.get_keywords()
deviation = 0.25 # 0.25 by default | relation of distance to word length
process_count = 3
################################
morph = pymorphy3.MorphAnalyzer()

if __name__ == '__main__':
	text = clear_text()
	# print(' '.join(text))
	# print(text)
	# exit()
	part_piece = math.floor(len(keywords)/process_count)
	keyword_parts = []
	for i in range(process_count):
		if i + 1 == process_count:
			keyword_parts.append(keywords[ part_piece*i : ])
		else:
			keyword_parts.append(keywords[ part_piece*i : part_piece*(i+1) ])

	threads = [
				Process(target=process_keywords_parts, args=(i+1, text, keyword_parts[i]))
				for i in range(process_count-1)
			]
	for thread in threads:
		thread.start()

	process_keywords_parts(process_count, text, keyword_parts[-1])

	for thread in threads:
		thread.join()

	print(cached_dist.cache_info())
	print(cached_morph.cache_info())
	cached_dist.cache_clear()
	cached_morph.cache_clear()