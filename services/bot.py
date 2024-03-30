import logging
from typing import Literal
import telegram.error
from telegram import ChatMember, Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from exceptions import UnauthorizedChatError
from exceptions.errors import UnauthorizedMemberError
from utils.parser import PropertyParser
from . import BotConfig


class BotAuthorizationService:

    def __init__(self, botconfig: BotConfig, context: ContextTypes.DEFAULT_TYPE):
        self._botconfig = botconfig
        self._context = context

    def is_user_in_conversation_restricted_to_groups(
        self, user_id: int, conversation: str
    ) -> bool:
        # Get conversation restricted group
        if not self._botconfig.conversations[conversation].restricted_to_groups:
            return True
        for group in self._botconfig.conversations[conversation].restricted_to_groups:
            if (user_id in self._botconfig.groups[group]) is True:
                return True
        return False

    def is_chat_in_command_whitelist(self, chat_id: int, command: str) -> bool:
        parser = PropertyParser(self._botconfig)
        chats_whitelist = [
            int(parser.parse(chat_key))
            for chat_key in self._botconfig.commands.get(command).chats_whitelist
        ]
        result = chat_id in chats_whitelist
        logging.info(
            f"check if chat_id={chat_id} is in chats_whitelist={chats_whitelist}: {result}"
        )
        return result

    def is_coming_from_authorized_chats(self, chat_id: int) -> bool:
        """Verify that the request issued to the bot is coming from an authorized chat.

        Args:
            chat_id (str | int): chat id where the request is issued

        Returns:
            bool: True if the chat is authorized else False
        """
        return chat_id in self._botconfig.chats.values()

    async def is_user_member_of_chat(self, user_id: int, chat_id: int) -> Literal[True]:
        try:
            member: ChatMember = await self._context.bot.get_chat_member(
                chat_id, user_id
            )
            logging.info(f"@{member} in chat_id={chat_id}")
            if member.status == ChatMember.LEFT:
                logging.warn(
                    f"user_id={member.user.id} is not part of chat_id={chat_id}"
                )
                raise UnauthorizedMemberError(chat_id, user_id)
            return True
        except telegram.error.BadRequest:
            logging.error(
                f"Bad request occured for user_id={user_id} and chat_id={chat_id}"
            )
            raise UnauthorizedMemberError(chat_id, user_id)

    async def is_user_member_of_authorized_chats(self, user_id: int) -> list[str]:
        authorized_chats = []
        for authorized_chat_id in self._botconfig.chats.values():
            try:
                await self.is_user_member_of_chat(user_id, authorized_chat_id)
                authorized_chats.append(authorized_chat_id)
            except UnauthorizedMemberError as err:
                logging.warn(err.message)
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

    async def notify_authorized_chats_where_user_is_member(
        self,
        user_id,
        message,
        message_type: ParseMode = ParseMode.MARKDOWN,
    ):
        """Send message from the Bot account to all authorized chat where the user
        that issued the command is a member

        If a user is reaching the bot via a chat that is not authorized by the botconfig, an error is raised.

        Args:
            user_id (int) : user id
            message (str): message to send
            message_type (ParseMode, optional): type of message. Defaults to ParseMode.MARKDOWN_V2.

        Raises:
            UnauthorizedChatError: unauthorized chat id
        """
        member_chats = (
            await self._authorization_service.is_user_member_of_authorized_chats(
                user_id
            )
        )
        for chat_id in member_chats:
            await self._context.bot.send_message(
                chat_id, text=message, parse_mode=message_type
            )
