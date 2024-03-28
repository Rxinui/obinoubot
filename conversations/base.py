import logging
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, ContextTypes, CommandHandler
from utils.parser import PropertyParser
from utils.botconfig import BotConfig


class BaseConversation:
    def __init__(
        self,
        botconfig: BotConfig,
        name: str,
        entry_points: list[CommandHandler],
        states: dict[int, list],
        fallbacks: list[CommandHandler],
    ):
        super().__init__()
        self._botconfig = botconfig
        self._name = name
        self._parser = PropertyParser(botconfig)
        self._entry_points = entry_points
        self._states = states
        self._fallbacks = fallbacks

    @property
    def name(self) -> str:
        return self._name

    @property
    def command_name(self) -> str:
        return f"/{self._name}"

    @property
    def handler(self) -> ConversationHandler:
        return ConversationHandler(self._entry_points, self._states, self._fallbacks)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        pass
