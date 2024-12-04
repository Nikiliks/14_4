import sqlite3

connection = sqlite3.connect('telebot_data.db')
cursor = connection.cursor()


def initiate_db():
    cursor.execute("""CREATE TABLE IF NOT EXISTS Products (
                        id INTEGER PRIMERY KEY,
                        title TEXT NOT NULL,
                        description TEXT,
                        price INTEGER NOT NULL
                    )""")
    connection.commit()
initiate_db()


cursor.execute('DELETE FROM Products')
for num in range(1, 5):
    cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                   (f'Продукт {num}', f'Описание {num}', num*100))
    connection.commit()

def get_all_products():
    cursor.execute('SELECT * FROM Products')
    return cursor.fetchall()
