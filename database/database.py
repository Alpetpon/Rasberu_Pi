from datetime import datetime
import aiosqlite


async def create_users():
    async with aiosqlite.connect('userdata.db') as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, "
            "username TEXT, comment TEXT, role TEXT, daily_limit INTEGER DEFAULT 0, monthly_limit INTEGER DEFAULT 0, "
            "yearly_limit INTEGER DEFAULT 0, last_action TIMESTAMP, permissions TEXT DEFAULT 0  )")
        await db.commit()
async def create_logs():
    async with aiosqlite.connect('userdata.db') as db:
        await db.execute('CREATE TABLE IF NOT EXISTS logs (user_id INTEGER, username TEXT, action TEXT, last_action TIMESTAMP)')
        await db.commit()

async def create_all_users():
    async with aiosqlite.connect('userdata.db') as db:
        await db.execute('CREATE TABLE IF NOT EXISTS all_users (user_id INTEGER PRIMARY KEY, username TEXT)')
        await db.commit()
async def create_banned():
    async with aiosqlite.connect('userdata.db') as db:
        await db.execute('CREATE TABLE IF NOT EXISTS banned (user_id INTEGER PRIMARY KEY, username TEXT)')
        await db.commit()
async def create_reg_word():
    async with aiosqlite.connect('userdata.db') as db:
        await db.execute('CREATE TABLE IF NOT EXISTS reg_word (word TEXT)')
        await db.commit()


async def add_user_to_all_user_table(user_id: str, username: str):
    async with aiosqlite.connect('userdata.db') as db:
        await db.execute("INSERT OR IGNORE INTO all_users VALUES (?, ?)", (user_id, username))
        await db.commit()


async def add_user_to_users_table(user_id: str, username: str, comment: str, role: str, current_time, permis):
    async with aiosqlite.connect('userdata.db') as db:
        await db.execute(
            'INSERT OR IGNORE INTO users (user_id, username, comment, role, last_action, permissions)'
            ' VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, username, comment, role, current_time, permis))
        await db.commit()


async def if_username_in_user_table():
    async with aiosqlite.connect('userdata.db') as conn:
        cursor = await conn.execute(f"SELECT username FROM users")
        row = await cursor.fetchall()
    return row


# вспомогательная функция для выборки user_id из таблицы all_users
# по username для дальнейшей регистрации пользователя админом
async def get_user_id_from_all_users_table(username):
    async with aiosqlite.connect('userdata.db') as conn:
        cursor = await conn.execute(f'SELECT user_id FROM all_users WHERE username=?', (username,))
        row = await cursor.fetchall()
    return row[0][0]


async def add_user_by_admin_to_user_table(user_id, username, comment, role, current_time, permis):
    async with aiosqlite.connect('userdata.db') as db:
        await db.execute('INSERT INTO users (user_id, username, comment, role, last_action, permissions)'
                         'VALUES (?,?,?,?,?,?)', (user_id, username, comment, role, current_time, permis))
        await db.commit()


# для генерации кнопок в зависимости от разрешений
async def get_permissions_info_from_users(user_id):
    async with aiosqlite.connect('userdata.db') as conn:
        cursor = await conn.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
        row = await cursor.fetchall()
    return row


async def all_info_about_users_button():
    async with aiosqlite.connect('userdata.db') as conn:
        cursor = await conn.execute('SELECT * FROM users')
        row = await cursor.fetchall()
    for i in range(len(row)):
        row[i] = list(row[i])
        row[i][0] = str(row[i][0])
        row[i][4] = str(row[i][4])
        row[i][5] = str(row[i][5])
        row[i][6] = str(row[i][6])
    return row

async def add_logs(user_id,username, text, current_time):
    async with aiosqlite.connect('userdata.db') as db:
        await db.execute('INSERT INTO logs (user_id, username, action, last_action) VALUES (?,?,?,?)', (user_id, username, text, current_time))
        await db.commit()

async def change_last_action_in_users_table(user_id, currnet_time):
    async with aiosqlite.connect('userdata.db') as db:
        await db.execute('UPDATE users SET last_action = ? WHERE user_id = ?', (currnet_time, user_id))
        await db.commit()

async def change_comment_in_table_users(username, comment):
    async with aiosqlite.connect('userdata.db') as db:
        await db.execute(f'UPDATE users SET comment = ? WHERE username = ?', (comment, username))
        await db.commit()

async def change_role_in_table_users(username, role):
    async with aiosqlite.connect('userdata.db') as db:
        await db.execute(f'UPDATE users SET role = ? WHERE username = ?', (role, username))
        await db.commit()

async def change_limits_in_table_users(username, daily_limit, monthly_limit, yearly_limit):
    async with aiosqlite.connect('userdata.db') as db:
        await db.execute(f'UPDATE users SET daily_limit = ?, monthly_limit = ?, yearly_limit = ?  WHERE username = ?', (daily_limit, monthly_limit,yearly_limit, username))
        await db.commit()

async def delete_user(username):
    async with aiosqlite.connect('userdata.db') as db:
        await db.execute('DELETE FROM users WHERE username = ?', (username,))
        await db.commit()

async def add_banned_user(username):
    async with aiosqlite.connect('userdata.db') as db:
        cursor = await db.execute('SELECT user_id FROM users WHERE username = ?', (username,))
        row = await cursor.fetchall()
        print(row)
    async with aiosqlite.connect('userdata.db') as db:
        await db.execute('INSERT OR IGNORE INTO banned VALUES (?, ?)', (row[0][0], username))
        await db.commit()

async def get_banned_id():
    async with aiosqlite.connect('userdata.db') as db:
        cursor = await db.execute('SELECT user_id FROM banned')
        row = await cursor.fetchall()
    return row

async def add_reg_word(word):
    async with aiosqlite.connect('userdata.db') as db:
        await db.execute('INSERT INTO reg_word VALUES (?)', (word,))
        await db.commit()

async def update_word(word):
    async with aiosqlite.connect('userdata.db') as db:
        await db.execute('UPDATE reg_word SET word = ?', (word,))
        await db.commit()

async def select_word():
    async with aiosqlite.connect('userdata.db') as conn:
        cursor = await conn.execute('SELECT * FROM reg_word')
        row = await cursor.fetchall()
    return row

async def delete_word():
    async with aiosqlite.connect('userdata.db') as db:
        await db.execute('DELETE FROM reg_word')
        await db.commit()

async def select_limits(user_id):
    async with aiosqlite.connect('userdata.db') as db:
        cursor = await db.execute('SELECT daily_limit, monthly_limit, yearly_limit FROM users WHERE user_id = ?', (user_id,))
        row = await cursor.fetchall()
    return row
