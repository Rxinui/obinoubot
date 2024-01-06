import logging
import json
import pytz
import telegram

from commands import get_commands
from utils import JobManager
from telegram.ext import ApplicationBuilder, ContextTypes, ExtBot
from telegram import MenuButton
from datetime import time, timezone

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

DEFAULT_TIMEZONE = pytz.timezone("Europe/Paris")

with open("bot.json") as botconfig:
    BOT_CONFIG = json.load(botconfig)

if __name__ == "__main__":
    with open("token") as token_fp:
        TOKEN_BOT = token_fp.read()
        application = ApplicationBuilder().token(TOKEN_BOT).build()
        bot : ExtBot = application.bot
        job_queue = application.job_queue
        JobManager.configure_jobs_scheduler(job_queue, BOT_CONFIG["scheduler"])
        for command in get_commands(BOT_CONFIG):
            application.add_handler(command.handler)
            logging.info(f"main: add handler {command.command_name}")
        menu = MenuButton(telegram.MenuButtonDefault)
        bot.set_chat_menu_button(chat_id="-1001959905789",menu_button=menu)
        application.run_polling()
