import logging
from telegram.ext import ContextTypes
from utils.botconfig import BotConfig


class BaseJob:
    def __init__(self, botconfig: BotConfig, name: str = None) -> None:
        self._botconfig = botconfig
        self._chats = self._botconfig.chats
        self.name = name

    @property
    def name(self) -> str:
        return self.__name__

    @name.setter
    def name(self, name: str):
        self.__name__ = name

    def __call__(self, context: ContextTypes.DEFAULT_TYPE):
        logging.info(f"{self.name} job is fired.")
