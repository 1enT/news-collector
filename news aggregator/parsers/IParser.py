import abc

class IParser(abc.ABC):
	@abc.abstractmethod
	def fix_last_new():
		""" Fix last publish news """

	@abc.abstractmethod
	def find_last_news():
		""" Find recently published news """

	# @abc.abstractmethod
	# def __parse_news_body():
	# 	""" Supportive method that helps parse news body """

	# @abc.abstractmethod
	# def __recursive_children_search():
	# 	""" Supportive method that helps parse news body """

	@abc.abstractmethod
	def get_last_news():
		""" Get news in a readable way """

	@abc.abstractmethod
	def drop_last_news():
		""" Clear last news stock """

	@abc.abstractmethod
	def current_new():
		""" Get current fixed news """