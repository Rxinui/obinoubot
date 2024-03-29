import logging
from telegram import Update
from telegram.ext import ContextTypes
from commands.base import BaseMessageCommand
from utils.botconfig import BotConfig


class PingCommand(BaseMessageCommand):

    def __init__(self, botconfig: BotConfig, name: str):
        super().__init__(botconfig, name, message_type="MARKDOWN")

    async def execute(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs
    ):
        logging.warning("PONG")
