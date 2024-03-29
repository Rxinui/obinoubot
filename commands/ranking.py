from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from commands.base import BaseMessageCommand
from exceptions.errors import CommandNotAllowedError
from utils.botconfig import BotConfig
from typing import Self


class RankingCommand(BaseMessageCommand):

    def __init__(self, botconfig: BotConfig, name: str):
        super().__init__(botconfig, name, message_type="MARKDOWN")

    async def execute(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs
    ):
        chat_key = self._botconfig.inverted_chats[str(update.message.chat_id)]
        link = self._botconfig.properties[chat_key].GSHEET_RANKING
        self.message = f"[Check out {update.effective_chat.title}'s ranking]({link})"
        # get property according to chat id
        await super().execute(update, context)
