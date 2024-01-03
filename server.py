import logging

from commands import commands
from jobs import jobs
from telegram.ext import ApplicationBuilder, ContextTypes
from datetime import time, timezone
import pytz

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

DEFAULT_TIMEZONE = pytz.timezone("Europe/Paris")

async def cb(context: ContextTypes.DEFAULT_TYPE):
    logging.info("SCHEDULED")
    await context.bot.send_message(chat_id="-1001959905789", text='One message every 5s')

if __name__ == "__main__":
    with open("token") as token_fp:
        TOKEN_BOT = token_fp.read()
        application = ApplicationBuilder().token(TOKEN_BOT).build()
        job_queue = application.job_queue
        for job in jobs:
            print(job.__name__)
            job_queue.run_repeating(job,interval=5,first=5)
        for command in commands:
            application.add_handler(command.handler)
            logging.info(f"main: add handler {command.command_name}")

        application.run_polling()
