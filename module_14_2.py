import sqlite3

connectin = sqlite3.connect("not_telegram_1.db")
cursor = connectin.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

for i in range(10):
    cursor.execute("INSERT INTO Users(username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (f'User{i + 1}', f'example{i + 1}@gmail.com', ((i + 1) * 10), 1000)
                   )

for i in range(1, 10, 2):
    cursor.execute("UPDATE Users SET balance = ? WHERE id = ?",
                   (500, i)
                   )

for i in range(1, 11, 3):
    cursor.execute("DELETE FROM Users WHERE id = ?", (i,))

cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != ?", (60,))
users = cursor.fetchall()
for user in users:
    print(f'Имя: {user[0]} | Почта: {user[1]} | Возраст: {user[2]} | Баланс: {user[3]}')

cursor.execute("DELETE FROM Users WHERE id = ?", (6,))

cursor.execute("SELECT COUNT(*) FROM Users")
Users_record_count = cursor.fetchone()[0]
print(f'\nКоличество записей в базе "Users" стало = {Users_record_count}')

cursor.execute("SELECT SUM(balance) FROM Users")
All_Users_balance = cursor.fetchone()[0]
print(f'Сумма всех балансов пользователей в базе "Users" = {All_Users_balance}')

cursor.execute("SELECT AVG(balance) FROM Users")
Users_balance_Average = cursor.fetchone()[0]
print(f'Средний баланс пользователей в базе Users = {Users_balance_Average}')

connectin.commit()
connectin.close()
