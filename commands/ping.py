from telegram import ChatMember, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from commands.base import BaseMessageCommand
from exceptions.errors import CommandNotAllowedError
from utils.botconfig import BotConfig
from typing import Self
from telegram.error import BadRequest


class PingCommand(BaseMessageCommand):

    def __init__(self, botconfig: BotConfig, name: str):
        super().__init__(botconfig, name, message_type="MARKDOWN")

    async def execute(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs
    ):
        try:
            member: ChatMember = await context.bot.get_chat_member(
                update.effective_chat.id, "5687897355"
            )
            self.message = f"{member.user.username}"
            print(member.to_dict())
        except BadRequest as error:
            self.message = f"Member not found"
        # get property according to chat id
        await super().execute(update, context)
