# -*- coding: utf-8 -*-
import telebot


bot = telebot.TeleBot("6012282382:AAG4RclgeGuSxpadCw6MiQQPH4aGblF5LVI")

bot.send_photo('@tatarnewss', "https://cdna.artstation.com/p/assets/images/images/005/369/648/large/viktor-cemboran-screenshot000.jpg?1490560391", caption="321")
exit()
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text == "Hi":
        bot.send_message(message.from_user.id, "Hello! I am HabrahabrExampleBot. How can i help you?")
    
    elif message.text == "How are you?" or message.text == "How are u?":
        bot.send_message(message.from_user.id, "I'm fine, thanks. And you?")
    
    else:
        bot.send_message(message.from_user.id, "Sorry, i dont understand you.")

bot.polling(none_stop=True, interval=0)

# Обработчик команд '/start' и '/help'.
@bot.channel_post_handler()
def handle_start_help(message):
    bot.send_message('111')
