from bdfunctions import *
import telebot
from telebot import apihelper, types
import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)
adminid = int(os.getenv("ADMIN_ID"))
password = os.getenv("PASSSWORD")
conn = sqlite3.connect('order.db', check_same_thread=False)


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id == adminid:

        markup = types.InlineKeyboardMarkup()
        menu = types.InlineKeyboardButton('Меню', callback_data='menu')
        markup.add(menu)
        bot.send_message(message.chat.id, 'Вы успешно вошли как администратор', reply_markup=markup)

    else:
        bot.send_message(message.chat.id, 'Вы успешно вошли как пользователь')


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'menu':
        markup2 = types.InlineKeyboardMarkup()
        adddate = types.InlineKeyboardButton('Добавить данные', callback_data='add')
        outostdate = types.InlineKeyboardButton('Вывести данные', callback_data='outpost')
        markup2.add(adddate, outostdate)
        bot.send_message(callback.message.chat.id, 'Вы успешно зашли в меню', reply_markup=markup2)

    if callback.data == 'add':
        markup3 = types.InlineKeyboardMarkup()
        dishesbtn = types.InlineKeyboardButton('dishes', callback_data='dishesadd')
        ordersbtn = types.InlineKeyboardButton('orders', callback_data='ordersadd')
        userbtn = types.InlineKeyboardButton('user', callback_data='useradd')
        markup3.add(dishesbtn, ordersbtn, userbtn)
        bot.send_message(callback.message.chat.id, 'Выберите бд', reply_markup=markup3)

    if callback.data == 'outpost':
        markup4 = types.InlineKeyboardMarkup()
        dishesbtn = types.InlineKeyboardButton('dishes', callback_data='dishesout')
        ordersbtn = types.InlineKeyboardButton('orders', callback_data='ordersout')
        userbtn = types.InlineKeyboardButton('user', callback_data='userout')
        markup4.add(dishesbtn, ordersbtn, userbtn)
        bot.send_message(callback.message.chat.id, 'Выберите бд', reply_markup=markup4)

    # ЗАПОЛНЕНИЕ БД DISHES
    if callback.data == 'dishesadd':
        data = bot.send_message(callback.message.chat.id, 'Введите название блюда, цену')
        bot.register_next_step_handler(data, filling_db_dishes)

    # ЗАПОЛНЕНИЕ БД orders
    if callback.data == 'ordersadd':
        data = bot.send_message(callback.message.chat.id, 'Введите колво, сумму в рублях, время заказа')
        bot.register_next_step_handler(data, filling_db_orders)

    # ЗАПОЛНЕНИЕ БД user
    if callback.data == 'useradd':
        data = bot.send_message(callback.message.chat.id, 'Введите персональную скидку, колвозаказов, любимое блюдо')
        bot.register_next_step_handler(data, filling_db_user)

    # ВЫВОДДАННЫХ bd dishes

    if callback.data == 'dishesout':
        bot.send_message(callback.message.chat.id, 'Вывожу список данных bd dishes')
        cos = conn.cursor()
        sqlite_select_query = """SELECT * from dishes"""
        cos.execute(sqlite_select_query)
        records = cos.fetchall()
        bot.send_message(callback.message.chat.id, 'Всепго строк: ' + str(len(records)))
        i = 1
        for row in records:
            bot.send_message(callback.message.chat.id,
                             'ID:' + str(i) + ';namedish: ' + row[0] + ';price:' + row[1] + '\n\n')
            i += 1

    # ВЫВОДДАННЫХ bd orders

    if callback.data == 'ordersout':
        bot.send_message(callback.message.chat.id, 'Вывожу список данных bd orders')
        cos = conn.cursor()
        sqlite_select_query = """SELECT * from orders"""
        cos.execute(sqlite_select_query)
        records = cos.fetchall()
        bot.send_message(callback.message.chat.id, 'Всепго строк: ' + str(len(records)))
        i = 1
        for row in records:
            bot.send_message(callback.message.chat.id,
                             'ID:' + str(i) + ';countdish: ' + row[0] + ';suminrubles:' + row[1] + ';timeorder: ' + row[
                                 2] + '\n\n')
            i += 1

    # ВЫВОДДАННЫХ bd user

    if callback.data == 'userout':
        bot.send_message(callback.message.chat.id, 'Вывожу список данных bd user')
        cos = conn.cursor()
        sqlite_select_query = """SELECT * from user"""
        cos.execute(sqlite_select_query)
        records = cos.fetchall()
        bot.send_message(callback.message.chat.id, 'Всепго строк: ' + str(len(records)))
        i = 1
        for row in records:
            bot.send_message(callback.message.chat.id,
                             'ID:' + str(i) + ';persondiscount: ' + row[0] + ';amountoforders:' + row[
                                 1] + ';preferreddish: ' + row[2] + '\n\n')
            i += 1


bot.polling(none_stop=True)
