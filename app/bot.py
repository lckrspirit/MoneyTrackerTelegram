#!/bin/python3

import os
import telebot
import sqlite3
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


load_dotenv()



bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
allow_users = [139654828]
categories = ["taxi", "homecredit", "bar", "transport", "coffie", "games", "home", "internet", "phone"]
category = ""

start_menu = '''
/new - Внести новый расход 🖊
/stats - Сколько было потрачено сегодня 📊
/ping - Чекнуть связь с ботом.
/categories - Список катерогий. 
'''

def insert_dbdata(sql):
    try:
        db = sqlite3.connect('db/moneytrk.db')
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
    except ValueError:
        print("Db problems..")
    

def grep_dbdate(sql):
    try:
        db = sqlite3.connect('db/moneytrk.db')
        cursor = db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()[0]
    except ValueError:
        print("Db problems..")


def get_stats():
    message = f"Потрачено сегодня..💸 \n--\n"
    sql_req = f"SELECT count(amount), sum(amount) from transactions WHERE date >= datetime('now');"
    amount, transactions = grep_dbdate(sql_req)
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
            msg = bot.reply_to(message, 'Error. Categor')
            bot.register_next_step_handler(msg, new_category(msg))
        else:
            insert_dbdata(f"INSERT INTO transactions(date, category, amount) VALUES(datetime('now','localtime'),\'{category}\',{amount});")
            msg = bot.reply_to(message, f"Добавлено 🤝")
    else:
        msg = bot.reply_to(message, "Not correct data. Try again.. ❌")


@bot.message_handler(commands=['ping'])
def ping(message):
    bot.send_message(message.chat.id, "pong 🪃")


@bot.message_handler(commands=['categories'])
def send_categories(message):
    answer = "Categories list: \n"
    for item in categories:
        answer += f" - {item}\n"
    bot.send_message(message.chat.id, answer)


if __name__ == '__main__':
    try:
        bot.infinity_polling()
    except ValueError:
        print("Ops..")