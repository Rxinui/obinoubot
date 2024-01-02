import logging
import json
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.constants import ParseMode

COMMAND_NAME = Path(__file__).stem

with open("bot.json") as properties_fp:
    BOT_PROPERTIES = json.load(properties_fp)["properties"]


async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_to_send = (
        f"*Entrer vos PRs [via ce formulaire]({BOT_PROPERTIES['GOOGLE_FORM_PR']})*"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text_to_send,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    logging.info(f"/{COMMAND_NAME} has been triggered")

# CommandHandler()