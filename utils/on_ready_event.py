from discord.ext import tasks
from discord_components import DiscordComponents

from loader import bot


@tasks.loop(count=1)
async def on_ready():
    """Функция on_ready выполняется при запуске бота и создаёт таблицу users
        в бд, также добавляет в бд имена, id, количество xp и сервер всех
        участников, которых нет в бд.
        """

    await bot.wait_until_ready()
    DiscordComponents(bot)

    print("Bot connected!")