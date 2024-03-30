from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from commands.base import BaseCommand
from utils.botconfig import BotConfig


class RankingCommand(BaseCommand):

    def __init__(self, botconfig: BotConfig, name: str):
        super().__init__(botconfig, name)

    async def execute(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs
    ):
        await super().execute(update, context)
        chat_key = self._botconfig.inverted_chats[update.message.chat_id]
        url = self._botconfig.properties[chat_key].GSHEET_RANKING
        message = f"[Checkout {update.effective_chat.title}'s ranking]({url})"
        await update.message.reply_text(message, ParseMode.MARKDOWN)
