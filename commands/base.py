import json
from abc import ABCMeta, ABC, abstractmethod
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.constants import ParseMode

class Singleton(type, metaclass=ABCMeta):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class BaseCommand(metaclass=Singleton):

    with open("bot.json") as properties_fp:
        BOT_PROPERTIES = json.load(properties_fp)["properties"]

    def __init__(self, name: str = None, filename: str = None) -> None:
        super().__init__()
        if filename:
            self._name = Path(filename).stem
        if name:
            self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def command_name(self) -> str:
        return f"/{self._name}"

    @property
    def handler(self):
        return CommandHandler(self._name,self.execute)

    @abstractmethod
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass