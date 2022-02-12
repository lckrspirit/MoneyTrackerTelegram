#!/bin/python3

import os
import telebot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from menus import start_menu, categories

load_dotenv()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
allow_users = [139654828]


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id in allow_users:
        bot.send_message(message.chat.id, start_menu)
    else:
        bot.send_message(message.chat.id, "Вы не в списке разрешенных, пользователей..")
        print(message.chat.id)


@bot.message_handler(commands=['stats'])
def stats(message):
    if message.chat.id in allow_users:
        bot.send_message(message.chat.id, "Stats menu")
    else:
        bot.send_message(message.chat.id, "Вы не в списке разрешенных, пользователей..")
        print(message.chat.id)




if __name__ == '__main__':
    bot.polling()