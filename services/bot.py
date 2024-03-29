import logging
from typing import Literal
import telegram.error
from telegram import ChatMember, Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from exceptions import UnauthorizedChatError
from exceptions.errors import UnauthorizedMemberError
from utils import botconfig
from utils.parser import PropertyParser
from . import BotConfig


class BotAuthorizationService:

    def __init__(self, botconfig: BotConfig, context: ContextTypes.DEFAULT_TYPE):
        self._botconfig = botconfig
        self._context = context

    def is_coming_from_authorized_chats(self, chat_id: str | int) -> bool:
        """Verify that the request issued to the bot is coming from an authorized chat.

        Args:
            chat_id (str | int): chat id where the request is issued

        Returns:
            bool: True if the chat is authorized else False
        """
        return str(object=chat_id) in self._botconfig.chats.values()

    async def is_user_member_of_chat(
        self, user_id: int, chat_id: str | int
    ) -> Literal[True]:
        try:
            member: ChatMember = await self._context.bot.get_chat_member(
                chat_id, user_id
            )
            logging.info(f"@{member.user.username} is member of chat_id={chat_id}")
            return True
        except telegram.error.BadRequest:
            raise UnauthorizedMemberError(user_id)

    async def is_user_member_of_authorized_chats(self, user_id: int) -> list[str]:
        authorized_chats = []
        for authorized_chat_id in self._botconfig.chats.values():
            try:
                await self.is_user_member_of_chat(user_id, authorized_chat_id)
                authorized_chats.append(authorized_chat_id)
            except UnauthorizedMemberError:
                logging.warn(
                    f"user_id={user_id} not a member of authorized chat_id={authorized_chat_id}"
                )
        return authorized_chats


class BotMessageService:
    def __init__(
        self, botconfig: BotConfig, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        self._authorization_service = BotAuthorizationService(botconfig, context)
        self._botconfig = botconfig
        self._update = update
        self._context = context

    async def send_reply(
        self, message: str, message_type: ParseMode = ParseMode.MARKDOWN_V2
    ) -> None:
        """Send message by the bot when a request is issued by a user.

        If a user is reaching the bot via a chat that is not whitelisted by the botconfig, an error is raised.

        Args:
            message (str): message to send
            message_type (ParseMode, optional): type of message. Defaults to ParseMode.MARKDOWN_V2.

        Raises:
            UnauthorizedChatError: unauthorized chat id
        """
        if not self._authorization_service.is_coming_from_authorized_chats(
            self._update.effective_chat.id
        ):
            raise UnauthorizedChatError(self._update.effective_chat.id)
        await self._update.effective_message.reply_text(message, message_type)

    async def notify_chat(
        self,
        chat_id: str | int,
        message: str,
        message_type: ParseMode = ParseMode.MARKDOWN,
    ) -> None:
        """Send message by the bot when a request is issued by a user.

        If a user is reaching the bot via a chat that is not whitelisted by the botconfig, an error is raised.

        Args:
            chat_id (str|int) : Either chat id (int) or chat property defined in botconfig expressed as '${chats.<chat-key-id>}'
            message (str): message to send
            message_type (ParseMode, optional): type of message. Defaults to ParseMode.MARKDOWN_V2.

        Raises:
            UnauthorizedChatError: unauthorized chat id
        """
        if type(chat_id) == str:
            _chat_id = int(PropertyParser(self._botconfig).parse(chat_id))
        elif type(chat_id) == int:
            _chat_id = chat_id
        else:
            raise TypeError("***Expecting chat_id to be either 'str' or 'int' type")
        if not self._authorization_service.is_coming_from_authorized_chats(_chat_id):
            raise UnauthorizedChatError(_chat_id)
        logging.info(f"Notify chat id '{chat_id}': {message}")
        await self._context.bot.send_message(
            _chat_id, text=message, parse_mode=message_type
        )

    async def notify_authorized_chats_where_user_is_member(
        self,
        user_id,
        message,
        message_type: ParseMode = ParseMode.MARKDOWN,
    ):
        member_chats = (
            await self._authorization_service.is_user_member_of_authorized_chats(
                user_id
            )
        )
        for chat_id in member_chats:
            await self._context.bot.send_message(
                chat_id, text=message, parse_mode=message_type
            )
