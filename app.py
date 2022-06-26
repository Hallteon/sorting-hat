from data.config import BOT_TOKEN
from loader import bot
from utils.on_ready_event import on_ready
from utils.db_stuff.connect_db import connect


def on_startup():
    bot.remove_command("help")
    import handlers

    on_ready.start()


if __name__ == "__main__":
    on_startup()
    bot.run(BOT_TOKEN)
