import nltk
#from multiprocessing import Process
import math
import re
from datetime import datetime
import logging

import pymorphy3
import functools
from searcher_test import get_data

class Searcher:
	def __init__(self, deviation = 0.25, process_count = 1):
		self.keywords = self.__get_keywords()
		self.deviation = deviation # 0.25 by default | relation of distance to word length
		self.process_count = process_count
		self.morph = pymorphy3.MorphAnalyzer()

	def dump_text(self, text):
		self.text = text
		self.text = self.__clear_text()

	def initiate(self):
		part_piece = math.floor(len(self.keywords)/self.process_count)
		keyword_parts = []
		for i in range(self.process_count):
			if i + 1 == self.process_count:
				keyword_parts.append(self.keywords[ part_piece*i : ])
			else:
				keyword_parts.append(self.keywords[ part_piece*i : part_piece*(i+1) ])

		# self.threads = [
		# 			Process(target=process_keywords_parts, args=(i+1, self.text, keyword_parts[i], self.deviation))
		# 			for i in range(self.process_count)
		# 		]
		# for thread in self.threads:
		# 	thread.start()
		
		result = process_keywords_parts(self.process_count, self.text, keyword_parts[-1], self.deviation)
		
		# for thread in self.threads:
		# 	thread.join()
		return result

	def clear_cache(self):
		print(cached_dist.cache_info())
		print(cached_morph.cache_info())
		logging.info(cached_dist.cache_info())
		logging.info(cached_morph.cache_info())
		cached_dist.cache_clear()
		cached_morph.cache_clear()

	def __get_keywords(self):
		arr = []
		with open('keywords.txt', 'r', encoding='utf-8') as file:
			arr = file.read().splitlines()
			arr = [word for word in arr if word != '']
		return arr

	def __clear_text(self):
		cleared_text = []
		morph = pymorphy3.MorphAnalyzer()
		forbidden_types = {'NPRO', 'PRED', 'PREP', 'CONJ', 'PRCL', 'INTJ'}

		for word in self.text:
			word = word.lower()
			cleared_word = re.sub(r"[,.+–:;!?()\'\"@#№$%^&*\\/<>«»„“]", '', word)
			morph_type = cached_morph(self.morph, cleared_word)
			#if morph_type != None and morph_type not in forbidden_types:
			if cleared_word != '' and morph_type not in forbidden_types:
				cleared_text.append(cleared_word)
		return cleared_text

################################
def process_keywords_parts(num, text, words, deviation):
	result = False
	for keyword in words:
		keyword_len = len(keyword.split())
		for i in range(0, len(text) - keyword_len + 1):
			slice_of_text = text[i:i + keyword_len]
			keyword_splitted = keyword.lower().split()
			dist = 0
			for i in range(len(slice_of_text)):
				dist += cached_dist(keyword_splitted[i], slice_of_text[i])
			slice_of_text = ' '.join(slice_of_text)

			if dist/len(slice_of_text) <= deviation:
				print(f"{num} | {keyword} | {slice_of_text} | {str(dist)}")
				logging.info(f"{num} | {keyword} | {slice_of_text} | {str(dist)}")
				result = True
	return result


@functools.lru_cache(maxsize=2**14)
def cached_dist(keyword, word_of_slice):
	keyword = keyword.lower()
	dist = nltk.edit_distance(keyword, word_of_slice)
	return dist

@functools.lru_cache(maxsize=2**10)
def cached_morph(morph, cleared_word):
	return morph.parse(cleared_word)[0].tag.POS


if __name__ == '__main__':
	text = get_data.get_text('searcher_test/text 3.txt')
	searcher = Searcher(process_count=1)
	searcher.dump_text(text)
	searcher.initiate()
	
	print(cached_dist.cache_info())
	print(cached_morph.cache_info())
	cached_dist.cache_clear()
	cached_morph.cache_clear()