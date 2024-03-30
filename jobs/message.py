from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.parser import PropertyParser
from utils.botconfig import BotConfig
from .base import BaseJob
import uuid


class MessageJob(BaseJob):

    def __init__(
        self, botconfig: BotConfig, chat_id: int, message: str, name: str = None
    ) -> None:
        self.__parser = PropertyParser(botconfig)
        self.__chat_id = int(self.__parser.parse(str(chat_id)))
        self.__message = self.__parser.parse(message)
        job_name = (
            f"{self.__class__.__name__}.{self.__chat_id}.{str(uuid.uuid1())[:8]}"
            if not name
            else name
        )
        super().__init__(botconfig, job_name)

    async def __call__(self, context: ContextTypes.DEFAULT_TYPE):
        super().__call__(context)
        await context.bot.send_message(
            chat_id=self.__chat_id, text=self.__message, parse_mode=ParseMode.MARKDOWN
        )
