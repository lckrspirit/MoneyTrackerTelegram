#!/bin/python3

import os
import telebot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


load_dotenv()


bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
allow_users = [139654828]
categories = ["taxi", "homecredit", "bar", "transport", "coffie", "games", "home", "internet", "phone"]

start_menu = '''
/new - Внести новый расход 🖊
/stats - Сколько было потрачено сегодня 📊
/ping - Чекнуть связь с ботом. 
'''


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
def get_transactions(message):
    msg = bot.reply_to(message, "Укажите потраченную сумму и категорию.. 🔥")
    bot.register_next_step_handler(msg, check_transactios)


def check_transactios(message):
    message_list = message.text.split()
    if len(message_list) == 2:
        amount = message_list[0]
        category = message_list[1]
        if category.lower() not in categories:
            msg = bot.reply_to(message, "Current category not found. Try again.. ❌")
            bot.register_next_step_handler(msg, get_transactions(msg))
        else:
            msg = bot.reply_to(message, "Done..")
    else:
        msg = bot.reply_to(message, "Not correct data. Try again.. ❌")


@bot.message_handler(commands=['ping'])
def ping(message):
    bot.send_message(message.chat.id, "pong 🪃")


if __name__ == '__main__':
    try:
        bot.infinity_polling()
    except ValueError:
        print("Ops..")