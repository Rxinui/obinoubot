import logging
import json
import pytz

from commands import commands
from utils import JobManager
from telegram.ext import ApplicationBuilder, ContextTypes
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
        job_queue = application.job_queue
        # Extract scheduler from bot.json
        # configure job listed
        JobManager.configure_jobs_scheduler(job_queue,BOT_CONFIG["scheduler"])
        # for command in commands:
        #     application.add_handler(command.handler)
        #     logging.info(f"main: add handler {command.command_name}")

        application.run_polling()
