import logging
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.constants import ParseMode

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

with open("bot.json") as properties_fp:
    BOT_PROPERTIES = json.load(properties_fp)["properties"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )
    logging.info("/pr has been triggered")


async def pr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_to_send = (
        f"*Entrer vos PRs [via ce formulaire]({BOT_PROPERTIES['GOOGLE_FORM_PR']})*"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text_to_send,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    logging.info("/pr has been triggered")

async def classement(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_to_send = (
        f"*[Voir le classement de l'équipage]({BOT_PROPERTIES['GOOGLE_SHEET_CLASSEMENT']})*"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text_to_send,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    logging.info("/classement has been triggered")


if __name__ == "__main__":
    with open("token") as token_fp:
        TOKEN_BOT = token_fp.read()
        application = ApplicationBuilder().token(TOKEN_BOT).build()
        start_handler = CommandHandler("start", start)
        pr_handler = CommandHandler("pr", pr)
        classement_handler = CommandHandler("classement", classement)
        application.add_handler(start_handler)
        application.add_handler(pr_handler)
        application.add_handler(classement_handler)

        application.run_polling()
