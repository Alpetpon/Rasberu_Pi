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


# Подключение к базе данных
def connect():
    return sqlite3.connect('bot_database.db')

# Функция проверки существования пользователя
def user_exists(user_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Функция добавления нового пользователя
def add_user(user_id, username, comment):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_id, username, comment) VALUES (?, ?, ?)", (user_id, username, comment))
    conn.commit()
    conn.close()


# Функция получения информации о пользователе
def get_user_info(user_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user_info = cursor.fetchone()
    conn.close()
    return user_info


# Функция получения имени пользователя по его ID
def get_username(user_id):
    user_info = get_user_info(user_id)
    return user_info[1] if user_info else None

# Функция обновления комментария пользователя
def update_user_comment(user_id, new_comment):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET comment=? WHERE user_id=?", (new_comment, user_id))
    conn.commit()
    conn.close()

# Функция получения всех пользователей в системе
def get_all_users():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    all_users = cursor.fetchall()
    conn.close()
    return all_users

# Функция удаления пользователя
def delete_user(user_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

# Функция добавления лога
def add_log(user_id, username, action):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (user_id, username, action) VALUES (?, ?, ?)", (user_id, username, action))
    conn.commit()
    conn.close()

# Функция получения всех логов
def get_all_logs():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    all_logs = cursor.fetchall()
    conn.close()
    return all_logs
