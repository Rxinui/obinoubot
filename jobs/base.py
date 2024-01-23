import logging
from telegram.ext import ContextTypes


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
