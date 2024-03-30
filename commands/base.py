import logging
from typing import Dict
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from exceptions.errors import CommandNotAllowedError
from services import BotMessageService
from services.bot import BotAuthorizationService
from utils.parser import PropertyParser
from utils.botconfig import BotConfig


class BaseCommand:
    def __init__(self, botconfig: BotConfig, name: str = None):
        super().__init__()
        self._botconfig = botconfig
        self._name = name
        self._parser = PropertyParser(botconfig)

    @property
    def name(self) -> str:
        return self._name

    @property
    def command_name(self) -> str:
        return f"/{self._name}"

    @property
    def handler(self) -> CommandHandler:
        return CommandHandler(self._name, self.execute)

    async def execute(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs
    ):
        logging.info(f"{self.command_name} has been triggered")
        auth_service = BotAuthorizationService(self._botconfig, context)
        if not auth_service.is_chat_in_command_whitelist(
            update.effective_chat.id, self.name
        ):
            raise CommandNotAllowedError(self.name, update.effective_chat.id)
        logging.info(
            f"{self.command_name} is authorized in chat_id={update.effective_chat.id}"
        )


class BaseMessageCommand(BaseCommand):
    MAP_MESSAGE_TYPE: Dict[str, ParseMode] = {
        "MARKDOWN": ParseMode.MARKDOWN,
        "MARKDOWN_V2": ParseMode.MARKDOWN_V2,
        "HTML": ParseMode.HTML,
    }

    def __init__(
        self,
        botconfig: BotConfig,
        name: str,
        message: str = "",
        message_type: str = "MARKDOWN_V2",
    ):
        super().__init__(botconfig, name)
        self._message = message
        self._message_type = self.MAP_MESSAGE_TYPE.get(message_type)

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, message: str):
        self._message = message

    async def execute(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs
    ):
        await super().execute(update, context)
        message = self._parser.parse(self._message)
        service = BotMessageService(self._botconfig, update, context)
        logging.info(f"{self.name} is sending message: {message}")
        await service.send_reply(message, self._message_type)
