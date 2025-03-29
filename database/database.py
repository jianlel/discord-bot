import aiosqlite
import datetime

DB_PATH = "database/wordle.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS streaks (
                user_id INTEGER PRIMARY KEY,
                daily_streak Integer, 
                streak INTEGER,
                wins INTEGER,
                losses INTEGER
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS daily_log (
                user_id INTEGER,
                date TEXT,
                PRIMARY KEY (user_id, date)
            )
        ''')
        await db.commit()


async def get_streak(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT streak FROM streaks WHERE user_id = ?', (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def get_wins(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT wins FROM streaks WHERE user_id = ?', (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def get_losses(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT losses FROM streaks WHERE user_id = ?', (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def user_exists(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT 1 FROM streaks WHERE user_id = ?', (user_id,)) as cursor:
            return await cursor.fetchone() is not None

async def win(user_id):
    if not await user_exists(user_id):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute('INSERT INTO streaks (user_id, streak, wins, losses) VALUES (?, ?, ?, ?)', (user_id, 1, 1, 0))
            await db.commit()
    else:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute('UPDATE streaks SET wins = wins + 1, streak = streak + 1 WHERE user_id = ?', (user_id,))
            await db.commit()

async def lose(user_id):
    if not await user_exists(user_id):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute('INSERT INTO streaks (user_id, streak, wins, losses) VALUES (?, ?, ?, ?)', (user_id, 0, 0, 1))
            await db.commit()
    else:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute('UPDATE streaks SET losses = losses + 1, streak = 0 WHERE user_id = ?', (user_id,))
            await db.commit()

async def reset_streak(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('UPDATE streaks SET streak = 0 WHERE user_id = ?', (user_id,))
        await db.commit()

async def get_daily_streak(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT daily_streak FROM streaks WHERE user_id = ?', (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def increment_daily_streak(user_id):
    if not await user_exists(user_id):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute('INSERT INTO streaks (user_id, streak, daily_streak, wins, losses) VALUES (?, ?, ?, ?, ?)', (user_id, 0, 1, 0, 0))
            await db.commit()
    else:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute('UPDATE streaks SET daily_streak = daily_streak + 1 WHERE user_id = ?', (user_id,))
            await db.commit()

async def reset_daily_streak(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('UPDATE streaks SET daily_streak = 0 WHERE user_id = ?', (user_id,))
        await db.commit()

async def has_played_today(user_id):
    today = str(datetime.date.today())
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT 1 FROM daily_log WHERE user_id = ? AND date = ?', (user_id, today)) as cursor:
            return await cursor.fetchone() is not None

async def mark_daily_completed(user_id):
    today = str(datetime.date.today())
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('INSERT OR IGNORE INTO daily_log (user_id, date) VALUES (?, ?)', (user_id, today))
        await db.commit()