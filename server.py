import logging
import pytz
import os
from telegram import Update

from telegram.ext import ApplicationBuilder, ContextTypes, ExtBot
from dotenv import load_dotenv
from utils import JobManager, BotConfig, CommandManager

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

DEFAULT_TIMEZONE = pytz.timezone("Europe/Paris")

def load_token():
    logging.info(f"APP_MODE is set on '{os.environ.get("APP_ENV")}'")
    if os.environ.get("APP_ENV") in ["prod","staging"]:
        return os.environ["TOKEN_BOT"]
    with open("token.staging", "r") as token_fp:
        return token_fp.read()
    
def load_botconfig() -> BotConfig:
    if os.environ.get("APP_ENV") == "prod":
        return BotConfig("bot.json")
    if os.environ.get("APP_ENV") == "staging":
        return BotConfig("bot.staging.json")
    return BotConfig("bot.staging.json")

def run():
    BOT_CONFIG = load_botconfig()
    application = ApplicationBuilder().token(load_token()).build()
    bot : ExtBot = application.bot
    JobManager.configure_jobs_scheduler(application.job_queue, BOT_CONFIG) # type: ignore
    commands = CommandManager.init_commands_from_botconfig(BOT_CONFIG)
    CommandManager.add_commands(application,commands)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    run()
