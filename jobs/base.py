import json
import logging
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

class BaseJob(metaclass=Singleton):

    with open("bot.json") as scheduler_fp:
        BOT_SCHEDULER = json.load(scheduler_fp)["scheduler"]

    def __init__(self) -> None:
        super().__init__()

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def __call__(self, context: ContextTypes.DEFAULT_TYPE):
        logging.info(f"{self.__name__} job is fired.")