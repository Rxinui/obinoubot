import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from .base import BaseCommand


class ClassementCommand(BaseCommand):
    def __init__(self) -> None:
        super().__init__(filename=__file__)

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text_to_send = f"*[Voir le classement de l'équipage]({self.BOT_PROPERTIES['GOOGLE_SHEET_CLASSEMENT']})*"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text_to_send,
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        logging.info(f"{self.command_name} has been triggered")
