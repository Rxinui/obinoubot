import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from .base import BaseCommand


class HelpCommand(BaseCommand):
    def __init__(self, botconfig: dict) -> None:
        super().__init__(botconfig, filename=__file__)

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text_to_send = (
            f"Les commandes disponibles sont :\n\n" \
            f"\pr - Formulaire des PRs a remplir\n"
            f"\classement - Feuille du classement\n"
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text_to_send,
            parse_mode=ParseMode.MARKDOWN,
        )
        logging.info(f"{self.command_name} has been triggered")
