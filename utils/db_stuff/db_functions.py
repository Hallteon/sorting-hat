from utils.db_stuff.connect_db import cursor, connect


async def create_table():
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                    name VARCHAR(255),
                    id BIGSERIAL NOT NULL PRIMARY KEY,
                    xp INT,
                    spam_warns INT);""")
    connect.commit()


async def select_xp(id):
    cursor.execute(f"""SELECT xp FROM users WHERE id = {id}""")

    return cursor.fetchone()[0]


async def select_top_users():
    cursor.execute(f"""SELECT name, xp FROM users ORDER BY xp DESC LIMIT 10;""")

    return cursor.fetchall()


async def add_xp_to_user(xp, id):
    cursor.execute(f"""UPDATE users SET xp = xp + {xp} WHERE id = {id};""")
    connect.commit()


async def add_user(user, id):
    try:
        cursor.execute(f"""INSERT INTO users VALUES ('{user}', {id}, {0}, {0}) ON CONFLICT DO NOTHING;""")

    except:
        return

    else:
        connect.commit()


async def remove_xp_from_user(xp, id):
    cursor.execute(f"""UPDATE users SET xp = xp - {xp} WHERE id = {id}""")
    connect.commit()


async def add_spam_warns(id):
    cursor.execute(f"""UPDATE users SET spam_warns = spam_warns + 1 WHERE id = {id};""")
    connect.commit()


async def get_warns(id):
    cursor.execute(f"""SELECT spam_warns FROM users WHERE id = {id};""")

    try:
        return cursor.fetchone()[0]

    except:
        pass


async def null_warns(id):
    cursor.execute(f"""UPDATE users SET spam_warns = 0 WHERE id = {id};""")
    connect.commit()