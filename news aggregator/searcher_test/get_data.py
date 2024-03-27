def get_text(src = 'text.txt'):
	text = ''
	with open(src, 'r', encoding='utf-8') as file:
		text = file.read().split()
	return text

def get_keywords():
	arr = []
	with open('keywords.txt', 'r', encoding='utf-8') as file:
		arr = file.read().splitlines()
		arr = [word for word in arr if word != '']
	return arr

if __name__ == '__main__':
	print( get_keywords() )