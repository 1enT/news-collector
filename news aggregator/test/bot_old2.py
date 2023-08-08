import requests

class Bot:
    def __init__(self):
        self.token = "6012282382:AAG4RclgeGuSxpadCw6MiQQPH4aGblF5LVI"
        self.url = 'https://api.telegram.org/bot'

    def send_post(self, mes):
        method = self.url + self.token + "/sendPhoto"
        message = "*{}*\n\n{}\n\n{}".format(mes['title'], mes['text'], mes['link'])
        if mes['img'] == None:
            self.__send_post_without_photo(message)
        else:
            r = requests.post(method, data = {
                    'chat_id': '@tatarnewss',
                    'photo': mes['img'],
                    'parse_mode': 'markdown',
                    'caption': message,
                    'disable_web_page_preview': True
                })
    def __send_post_without_photo(self, message):
        method = self.url + self.token + "/sendMessage"
        r = requests.post(method, data = {
                'chat_id': '@tatarnewss',
                'parse_mode': 'markdown',
                'text': message,
                'disable_web_page_preview': True
            })