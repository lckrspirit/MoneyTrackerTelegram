#!/bin/python3

import os
import telebot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from menus import start_menu, categories, new_transaction_title

load_dotenv()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
allow_users = [139654828]
user_dict = {"chat_id":""}


class transaction:
    def __init__(self, user):
        user = user
        amount = None
        category = None


def get_stats():
    message = f"Потрачено сегодня..💸 \n--\n"
    #Запрос в базу, посмотреть, где дергаем количество транзакция и сумму.
    amount, transactions = 400, 3
    message += f"Потрачено сегодня: {amount}\nТранзакции за сегодня: {transactions}"
    return message


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
        bot.send_message(message.chat.id, get_stats())
    else:
        bot.send_message(message.chat.id, "Вы не в списке разрешенных, пользователей..")


@bot.message_handler(commands=['new'])
def send_welcome(message):
    user = message.chat.id
    trs = transaction(user)
    user_dict['chat_id'] = trs
    msg = bot.send_message(message.chat.id, "Укажи потраченную сумму.. 👇👇👇")
    bot.register_next_step_handler(msg, get_categories)


def get_categories(message):
    msg = bot.send_message(message.chat.id, "Укажи категорию.. 👇👇👇")
    categories = message.text
    trs = user_dict['chat_id']
    trs.amount = message.text
    bot.register_next_step_handler(msg, check_transactios)


def check_transactios(message):
    trs = user_dict['chat_id']
    trs.category = message.text
    bot.reply_to(message, f"{trs.amount}, {trs.category}")
    

@bot.message_handler(commands=['ping'])
def ping(message):
    bot.send_message(message.chat.id, "pong 🪃")




if __name__ == '__main__':
    bot.polling()