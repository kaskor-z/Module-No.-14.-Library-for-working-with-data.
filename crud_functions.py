import sqlite3

TABLE_NAME = "Products"
USER_TABLE_NAME = "Users"

def initiate_db(Table_Name):
    connection = sqlite3.connect("not_telegram_2.db")
    cursor = connection.cursor()
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {Table_Name}('
                   f'id INTEGER PRIMARY KEY, '
                   f'title TEXT NOT NULL, '
                   f'description TEXT NOT NULL, '
                   f'file_image TEXT NOT NULL, '
                   f'price INTEGER NOT NULL'
                   f')'
                   )
    connection.commit()
    connection.close()


def initiate_db_Usr(User_Table_Name):
    connection = sqlite3.connect("not_telegram_3.db")
    cursor = connection.cursor()
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {User_Table_Name}('
                   f'id INTEGER PRIMARY KEY, '
                   f'username TEXT NOT NULL, '
                   f'email TEXT NOT NULL, '
                   f'age INTEGER NOT NULL, '
                   f'balance INTEGER NOT NULL'
                   f')'
                   )
    connection.commit()
    connection.close()


def add_user(*User_Data):
    connection = sqlite3.connect("not_telegram_3.db")
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO {USER_TABLE_NAME} (username, email, age, balance) "
                   f"VALUES(?, ?, ?, ?)", User_Data)
    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect("not_telegram_3.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT id FROM {USER_TABLE_NAME} WHERE username=?", (username,))
    User_exists = cursor.fetchone()
    return False if User_exists == None else True

    connection.commit()
    connection.close()


def set_products(*Data_Product):
    product_data = Data_Product
    connection = sqlite3.connect("not_telegram_2.db")
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO {TABLE_NAME} (title, description, file_image, price) "
                   f"VALUES(?, ?, ?, ?)", product_data)
    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect("not_telegram_2.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    return cursor.fetchall(); connection.close()


initiate_db_Usr(USER_TABLE_NAME)
initiate_db(TABLE_NAME)
set_products("Витамин Д3 D3 5000 МЕ НАУ 120 капсул",
             "Витамин Д3 — биологически активная добавка к пище, помогающая "
             "поддерживать нормальное функционирование большинства систем в организме человека, "
             "включая нервную, эндокринную и сердечно-сосудистую.", "./Витамины/1.png", 987
             )
set_products("Витамин Д3 5000 МЕ для костей и зубов",
             "Витамин д3 5000 ме - важнейшее питательное вещество, "
             "играющее важную роль во многих функциях организма. "
             "Одним из наиболее важных преимуществ этого витамина является "
             "его способность поддерживать здоровье костей.", "./Витамины/2.png", 721
             )
set_products("Витамин Д3 5000 vitamin d3 5000 (360 капсул)",
             "Витамин Д3 5000 ед в 1 капсуле. "
             "Общий объем витамин d3 в банке - 1 800 000 МЕ "
             "(360 капсул витамин д 5000 ме в 1 капсуле). "
             "Витамин Д 3 - это незаменимые витамины для иммунитета, синтезируется в "
             "клетках кожи под действие ультрафиолетовых лучей, усваивается с пищей. "
             "Вит Д3 регулирует обмен и уровень содержания кальция и фосфора в организме. "
             "d3 витамин предотвращает развитие остеопороза, "
             "повышает иммунитет.", "./Витамины/3.png", 546
             )
set_products("Витамин Д3 5000 МЕ и К2 100 мкг, 60 капсул",
             "Для компенсации дефицита витамина D3 можно принимать капсулы "
             "с высокой дозировке 5000 ME.Витамин Д3 к2 5000 "
             "с оптимальной дозировков витаминов для взрослых. "
             "Комплекс витамина д с к2 регулирует кальций-фосфорный обмен, "
             "усиливает всасывание кальция в кишечнике и реабсорбцию фосфора "
             "в почечных канальцах, нормализует формирование костного скелета и "
             "зубов у детей, витаминный комплекс способствует сохранению "
             "структуры костей.", "./Витамины/4.png", 683
             )

