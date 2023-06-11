import telebot
import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()

from telebot import apihelper, types

API_KEY=os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)
adminid= int(os.getenv("ADMIN_ID"))
password=os.getenv("PASSSWORD")
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id ==  adminid:
        markup = types.InlineKeyboardMarkup()
        menu=types.InlineKeyboardButton('Меню',callback_data='menu')
        markup.add(menu)
        bot.send_message(message.chat.id,'Вы успешно вошли как администратор',reply_markup=markup)

    else:
        bot.send_message(message.chat.id, 'Вы успешно вошли как пользователь')



@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data=='menu':
        markup2=types.InlineKeyboardMarkup()
        adddate = types.InlineKeyboardButton('Добавить данные', callback_data='add')
        outostdate = types.InlineKeyboardButton('Вывести данные', callback_data='outpost')
        markup2.add(adddate,outostdate)
        bot.send_message(callback.message.chat.id,'Вы успешно зашли в меню',reply_markup=markup2)
    if callback.data=='add':

        markup3 = types.InlineKeyboardMarkup()
        dishesbtn = types.InlineKeyboardButton('dishes', callback_data='dishesadd')
        ordersbtn = types.InlineKeyboardButton('orders', callback_data='ordersadd')
        userbtn = types.InlineKeyboardButton('user', callback_data='useradd')
        markup3.add(dishesbtn, ordersbtn, userbtn)
        bot.send_message(callback.message.chat.id, 'Выберите бд', reply_markup=markup3)
    if callback.data=='outpost':

        markup4 = types.InlineKeyboardMarkup()
        dishesbtn = types.InlineKeyboardButton('dishes', callback_data='dishesout')
        ordersbtn = types.InlineKeyboardButton('orders', callback_data='ordersout')
        userbtn = types.InlineKeyboardButton('user', callback_data='userout')
        markup4.add(dishesbtn, ordersbtn, userbtn)
        bot.send_message(callback.message.chat.id, 'Выберите бд', reply_markup=markup4)
    #ЗАПОЛНЕНИЕ БД DISHES
    if callback.data == 'dishesadd':
        data = bot.send_message(callback.message.chat.id, 'Введите название блюда, цену')

        def create_db(namedish,price):
            conn = sqlite3.connect('order.db')

            db_data = [(namedish,price)]
            conn.executemany("INSERT INTO dishes(namedish,price) VALUES (?, ?)", db_data)  # Запись данных в БД

            conn.commit()  # Сохранение данных в БД
            conn.close()
        @bot.message_handler()
        def filling_db_2(message):
            text = message.text.split(',')
            namedish = text[0]
            price = text[1]

            create_db(namedish, price)

        bot.register_next_step_handler(data, filling_db_2)

    # ЗАПОЛНЕНИЕ БД orders
    if callback.data == 'ordersadd':
        data = bot.send_message(callback.message.chat.id, 'Введите колво, сумму в рублях, время заказа')

        def create_db( countdish,suminrubles,  timeorder):
            conn = sqlite3.connect('order.db')

            db_data = [( countdish,suminrubles,  timeorder)]
            conn.executemany("INSERT INTO orders(countdish,suminrubles,timeorder) VALUES ( ?,?,?)", db_data)  # Запись данных в БД

            conn.commit()  # Сохранение данных в БД
            conn.close()
        @bot.message_handler()
        def filling_db_2(message):
            text = message.text.split(',')

            countdish = text[0]
            suminrubles = text[1]
            timeorder = text[2]

            create_db( countdish,suminrubles,  timeorder)

        bot.register_next_step_handler(data, filling_db_2)

# ЗАПОЛНЕНИЕ БД user

        def create_db(persondiscount, amountoforders,preferreddish):
            conn = sqlite3.connect('order.db')

            db_data = [(persondiscount, amountoforders,preferreddish)]
            conn.executemany("INSERT INTO user(persondiscount,amountoforders,preferreddish) VALUES (?, ?,?)", db_data)  # Запись данных в БД

            conn.commit()  # Сохранение данных в БД
            conn.close()
        @bot.message_handler()
        def filling_db_2(message):
            text = message.text.split(',')
            persondiscount = text[0]
            amountoforders = text[1]
            preferreddish = text[2]

            create_db(persondiscount, amountoforders,preferreddish)

        bot.register_next_step_handler(data, filling_db_2)


# ВЫВОДДАННЫХ bd dishes

    if callback.data == 'dishesout':
        data = bot.send_message(callback.message.chat.id, 'Вывожу список данных bd dishes')
        try:
            sqlite_connection = sqlite3.connect('order.db')
            conn = sqlite_connection.cursor()
            sqlite_select_query = """SELECT * from dishes"""
            conn.execute(sqlite_select_query)
            records = conn.fetchall()
            bot.send_message(callback.message.chat.id, 'Всепго строк: ' + str(len(records)))
            i = 1
            for row in records:
                bot.send_message(callback.message.chat.id, 'ID:' +str(i)+';namedish: '+ row[0]+';price:'+row[1]+'\n\n')
                i+=1

            conn.close()
        except sqlite3.Error as error:
            bot.send_message(callback.message.chat.id,"Ошибка при работе с SQLite:"+ error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                bot.send_message(callback.message.chat.id,"Соединение с SQLite закрыто")

    # ВЫВОДДАННЫХ bd orders

    if callback.data == 'ordersout':
        data = bot.send_message(callback.message.chat.id, 'Вывожу список данных bd orders')
        try:
            sqlite_connection = sqlite3.connect('order.db')
            conn = sqlite_connection.cursor()
            sqlite_select_query = """SELECT * from orders"""
            conn.execute(sqlite_select_query)
            records = conn.fetchall()
            bot.send_message(callback.message.chat.id, 'Всепго строк: ' + str(len(records)))
            i = 1
            for row in records:
                bot.send_message(callback.message.chat.id, 'ID:' +str(i)+';countdish: '+ row[0]+';suminrubles:'+row[1]+';timeorder: '+ row[2]+'\n\n')
                i+=1

            conn.close()
        except sqlite3.Error as error:
            bot.send_message(callback.message.chat.id,"Ошибка при работе с SQLite:"+ error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                bot.send_message(callback.message.chat.id,"Соединение с SQLite закрыто")

# ВЫВОДДАННЫХ bd user

    if callback.data == 'userout':
        data = bot.send_message(callback.message.chat.id, 'Вывожу список данных bd user')
        try:
            sqlite_connection = sqlite3.connect('order.db')
            conn = sqlite_connection.cursor()
            sqlite_select_query = """SELECT * from user"""
            conn.execute(sqlite_select_query)
            records = conn.fetchall()
            bot.send_message(callback.message.chat.id, 'Всепго строк: ' + str(len(records)))
            i = 1
            for row in records:
                bot.send_message(callback.message.chat.id, 'ID:' +str(i)+';persondiscount: '+ row[0]+';amountoforders:'+row[1]+';preferreddish: '+ row[2]+'\n\n')
                i+=1

            conn.close()
        except sqlite3.Error as error:
            bot.send_message(callback.message.chat.id,"Ошибка при работе с SQLite:"+ error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                bot.send_message(callback.message.chat.id,"Соединение с SQLite закрыто")


bot.polling(none_stop=True)
