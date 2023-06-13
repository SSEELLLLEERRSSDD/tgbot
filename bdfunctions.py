import sqlite3
conn = sqlite3.connect('order.db', check_same_thread=False)
# ЗАПОЛНЕНИЕ ТАБЛИЦЫ user
def filling_db_user(message):
    text = message.text.split(',')
    persondiscount = text[0]
    amountoforders = text[1]
    preferreddish = text[2]

    add_db_user(persondiscount, amountoforders, preferreddish)


# ЗАПОЛНЕНИЕ ТАБЛИЦЫ orders
def filling_db_orders(message):
    text = message.text.split(',')

    countdish = text[0]
    suminrubles = text[1]
    timeorder = text[2]

    add_db_orders(countdish, suminrubles, timeorder)


# ЗАПОЛНЕНИЕ ТАБЛИЦЫ dishes
def filling_db_dishes(message):
    text = message.text.split(',')
    namedish = text[0]
    price = text[1]
    add_db_dishes(namedish, price)


# ЗАПОЛНЕНИЕ БД dishes
def add_db_dishes(namedish, price):
    db_data = [(namedish, price)]
    conn.executemany("INSERT INTO dishes(namedish,price) VALUES (?, ?)", db_data)  # Запись данных в БД
    conn.commit()  # Сохранение данных в БД


# ЗАПОЛНЕНИЕ БД user
def add_db_user(persondiscount, amountoforders, preferreddish):
    db_data = [(persondiscount, amountoforders, preferreddish)]
    conn.executemany("INSERT INTO user(persondiscount,amountoforders,preferreddish) VALUES (?, ?,?)", db_data)
    conn.commit()


# ЗАПОЛНЕНИЕ БД orders
def add_db_orders(countdish, suminrubles, timeorder):
    db_data = [(countdish, suminrubles, timeorder)]
    conn.executemany("INSERT INTO orders(countdish,suminrubles,timeorder) VALUES ( ?,?,?)", db_data)
    conn.commit()
