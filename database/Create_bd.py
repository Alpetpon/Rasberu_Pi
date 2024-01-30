import sqlite3

# Создание подключения к базе данных (или создание файла, если он не существует)
conn = sqlite3.connect('bot_database.db')

# Создание курсора для выполнения SQL-запросов
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        action TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        comment TEXT,
        role TEXT DEFAULT 'user',
        daily_limit INTEGER DEFAULT 0,
        monthly_limit INTEGER DEFAULT 0,
        yearly_limit INTEGER DEFAULT 0,
        last_action_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (user_id)
    )
''')

conn.commit()
conn.close()
