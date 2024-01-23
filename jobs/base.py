import json
import logging
from utils import Singleton
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.constants import ParseMode


class BaseJob:
    def __init__(self, botconfig: dict, name: str = None) -> None:
        self.__botconfig = botconfig
        self._chats = self.__botconfig["chats"]
        self._name = name

    @property
    def BOT_SCHEDULER(self) -> dict:
        return self.__botconfig["scheduler"]

    @property
    def BOT_PROPERTIES(self) -> dict:
        return self.__bot_properties["properties"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def __call__(self, context: ContextTypes.DEFAULT_TYPE):
        logging.info(f"{self.__name__} job is fired.")


class BaseMessageJob(BaseJob):
    def __init__(
        self, botconfig: dict, chat_id: str, message: str, name: str = None
    ) -> None:
        super().__init__(botconfig, name)
        self.__chat_id = chat_id
        self.__message = message

    async def __call__(self, context: ContextTypes.DEFAULT_TYPE):
        super().__call__(context)
        await context.bot.send_message(
            chat_id=self.__chat_id, text=self.__message, parse_mode=ParseMode.MARKDOWN
        )
