import json
import logging
from utils import Singleton
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.constants import ParseMode



class BaseJob():

    def __init__(self) -> None:
        super().__init__()

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def __call__(self, context: ContextTypes.DEFAULT_TYPE):
        logging.info(f"{self.__name__} job is fired.")