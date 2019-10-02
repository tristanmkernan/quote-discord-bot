import os

from bot import bot
from bot.datastore.database import init_db

init_db()

bot.run(os.environ.get("BOT_PASSWORD"))
