import json
import re
import logging
from abc import ABCMeta, ABC, abstractmethod
from pathlib import Path
from typing import Dict
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from utils import PropertyParser

class BaseCommand:
    def __init__(self, botconfig: dict, name: str = None):
        super().__init__()
        self.__bot_properties = botconfig
        self._name = name

    @property
    def BOT_PROPERTIES(self) -> dict:
        return self.__bot_properties["properties"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def command_name(self) -> str:
        return f"/{self._name}"

    @property
    def handler(self) -> CommandHandler:
        return CommandHandler(self._name, self.execute)

    @abstractmethod
    async def execute(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs
    ):
        pass


class BaseMessageCommand(BaseCommand):
    MAP_MESSAGE_TYPE: Dict[str, ParseMode] = {
        "MARKDOWN": ParseMode.MARKDOWN,
        "MARKDOWN_V2": ParseMode.MARKDOWN_V2,
        "HTML": ParseMode.HTML,
    }

    def __init__(self, botconfig: dict, name: str, message: str, message_type: str):
        super().__init__(botconfig, name)
        self._message = message
        self._message_type = self.MAP_MESSAGE_TYPE.get(message_type)
        self._parser = PropertyParser(botconfig)


    async def execute(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs
    ):
        message = self._parser.parse(self._message)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode=self._message_type,
        )
        logging.info(f"{self.command_name} has been triggered")

    