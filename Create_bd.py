import sqlite3

# Создаем подключение к базе данных (если её нет, она будет автоматически создана)
conn = sqlite3.connect('mydatabase.db')

# Создаем объект курсора, который используется для выполнения SQL-запросов
cursor = conn.cursor()

# Создаем таблицу
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        email TEXT
    )
''')

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()
