import os
import requests
import telebot
from flask import Flask , request
from bs4 import BeautifulSoup # Модуль для работы с HTML
import time # Модуль для остановки программы
import datetime

TOKEN = '2001618640:AAE-bA_qXoY878BTKFj3iNFbMFXS8PfBaEE'
APP_URL = f'https://mfkbot.herokuapp.com/{TOKEN}'
bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo(message):
    bot.reply_to(message, message.text)


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return '!', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
