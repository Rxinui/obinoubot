from telegram import ChatMember, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from commands.base import BaseMessageCommand
from exceptions.errors import CommandNotAllowedError
from services.bot import BotMessageService
from utils.botconfig import BotConfig
from typing import Self
from telegram.error import BadRequest


class PingCommand(BaseMessageCommand):

    def __init__(self, botconfig: BotConfig, name: str):
        super().__init__(botconfig, name, message_type="MARKDOWN")

    async def execute(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs
    ):
        everyday_id = 5414239606
        service = BotMessageService(self._botconfig, update, context)
        await service.notify_authorized_chats_where_user_is_member(everyday_id, "OK")
