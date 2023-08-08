import telebot

class Bot:
    def __init__(self):
        self.bot = telebot.TeleBot("6012282382:AAG4RclgeGuSxpadCw6MiQQPH4aGblF5LVI")
        self.channel_id = "@tatartestnews"


    def send_post(self, mes):
        message = "*{}*\n\n{}\n\n{} {}".format(mes['title'], mes['lead'], mes['source'], mes['link'])
        if mes['img_url'] == None:
            self.bot.send_message(self.channel_id, message, parse_mode = "markdown", disable_web_page_preview = True)
        else:
            print(mes['img_url'])
            print(message)
            self.bot.send_photo(self.channel_id, mes['img_url'], parse_mode = "markdown", caption = message)
