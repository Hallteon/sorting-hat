from discord.ext import tasks
from discord_components import DiscordComponents

from data.config import BOTS_ID
from loader import bot
from utils.db_stuff.connect_db import cursor, connect


@tasks.loop(count=1)
async def on_ready():
    """Функция on_ready выполняется при запуске бота и создаёт таблицу users
        в бд, также добавляет в бд имена, id, количество xp и сервер всех
        участников, которых нет в бд."""

    await bot.wait_until_ready()
    DiscordComponents(bot)

    for guild in bot.guilds:
        for member in guild.members:
            if member.id not in BOTS_ID:
                cursor.execute(f"""INSERT INTO users VALUES ('{member}', {member.id}, {0}, {0}) ON CONFLICT DO NOTHING;""")

    connect.commit()

    print("Bot connected!")