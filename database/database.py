from datetime import datetime
import aiosqlite


async def create_database():
    async with aiosqlite.connect('userdata.db') as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, "
            "username TEXT, comment TEXT, role TEXT, daily_limit INTEGER DEFAULT 0, monthly_limit INTEGER DEFAULT 0, "
            "yearly_limit INTEGER DEFAULT 0, last_action TIMESTAMP, permissions TEXT DEFAULT 0  )")
        await db.commit()
        await db.execute(
            "CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER , "
            "username TEXT, action TEXT, stamp TIMESTAMP)")
        await db.commit()
        await db.execute('CREATE TABLE IF NOT EXISTS all_users (user_id INTEGER PRIMARY KEY, username TEXT)')
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
