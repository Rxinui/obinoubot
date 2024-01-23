import logging
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from utils import Singleton
from utils.parser import PropertyParser
from .base import BaseJob


class MessageJob(BaseJob, metaclass=Singleton):
    __name__ = "MessageJob"

    def __init__(
        self, botconfig: dict, chat_id: str, message: str, name: str = None
    ) -> None:
        super().__init__(botconfig, name)
        self.__parser = PropertyParser(botconfig)
        self.__chat_id = self.__parser.parse(chat_id)
        self.__message = self.__parser.parse(message)

    async def __call__(self, context: ContextTypes.DEFAULT_TYPE):
        super().__call__(context)
        await context.bot.send_message(
            chat_id=self.__chat_id, text=self.__message, parse_mode=ParseMode.MARKDOWN
        )
