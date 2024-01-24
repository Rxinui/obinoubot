import logging
from telegram.ext import ContextTypes
from utils.botconfig import BotConfig 


class BaseJob:
    def __init__(self, botconfig: BotConfig, name: str = None) -> None:
        self._botconfig = botconfig
        self._chats = self._botconfig.chats
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def __call__(self, context: ContextTypes.DEFAULT_TYPE):
        logging.info(f"{self.__name__} job is fired.")
