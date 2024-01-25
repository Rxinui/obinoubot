import logging
import pytz
import os

from telegram.ext import ApplicationBuilder, ContextTypes, ExtBot
from dotenv import load_dotenv
from utils import JobManager, BotConfig, CommandManager

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
    JobManager.configure_jobs_scheduler(application.job_queue, BOT_CONFIG)
    commands = CommandManager.init_commands_from_botconfig(BOT_CONFIG)
    CommandManager.add_commands(application,commands)
    application.run_polling()

if __name__ == "__main__":
    run()
