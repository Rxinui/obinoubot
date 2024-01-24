import logging
import pytz
import os

from telegram.ext import ApplicationBuilder, ContextTypes, ExtBot
from dotenv import load_dotenv
from commands import get_commands
from utils import JobManager, BotConfig

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

DEFAULT_TIMEZONE = pytz.timezone("Europe/Paris")

def load_token():
    logging.info(f"APP_MODE is set on '{os.environ.get("APP_ENV")}'")
    if os.environ.get("APP_ENV") == "prod":
        return os.environ["TOKEN_BOT"]
    with open("token") as token_fp:
        return token_fp.read()

def run():
    load_dotenv()
    BOT_CONFIG = BotConfig("bot.json")
    application = ApplicationBuilder().token(load_token()).build()
    bot : ExtBot = application.bot
    job_queue = application.job_queue
    JobManager.configure_jobs_scheduler(job_queue, BOT_CONFIG)
    for command in get_commands(BOT_CONFIG):
        application.add_handler(command.handler)
        logging.info(f"main: add handler {command.command_name}")
    application.run_polling()

if __name__ == "__main__":
    run()
