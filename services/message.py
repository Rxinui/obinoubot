import logging
import telegram.error
from telegram import ChatMember, Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from exceptions import UnauthorizedChatError
from utils import botconfig
from utils.parser import PropertyParser
from . import BotConfig


class BotMessage:

    def __init__(
        self,
        botconfig: BotConfig,
        update: Update = None,
        context: ContextTypes.DEFAULT_TYPE = None,
    ):
        self._botconfig = botconfig
        self._update = update
        self._context = context

    def _is_coming_from_authorized_chats(self, chat_id: str | int) -> bool:
        """Verify that the request issued to the bot is coming from an authorized chat.

        Args:
            chat_id (str | int): chat id where the request is issued

        Returns:
            bool: True if the chat is authorized else False
        """
        return str(chat_id) in self._botconfig.chats.values()


class BotReplyService(BotMessage):
    def __init__(
        self, botconfig: BotConfig, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        super().__init__(botconfig, update, context)

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
        if not self._is_coming_from_authorized_chats(self._update.effective_chat.id):
            raise UnauthorizedChatError(self._update.effective_chat.id)
        await self._update.effective_message.reply_text(message, message_type)


class BotNotifyService(BotMessage):
    def __init__(
        self, botconfig: BotConfig, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        super().__init__(botconfig, update, context)

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
        if not self._is_coming_from_authorized_chats(_chat_id):
            raise UnauthorizedChatError(_chat_id)
        logging.info(f"Notify chat id '{chat_id}': {message}")
        await self._context.bot.send_message(
            _chat_id, text=message, parse_mode=message_type
        )

    async def notify_authorized_chat_where_user_is_member(
        self,
        message,
        message_type: ParseMode = ParseMode.MARKDOWN,
    ):
        for authorized_chat_id in self._botconfig.chats.values():
            try:
                member: ChatMember = await self._context.bot.get_chat_member(
                    authorized_chat_id, self._update.effective_user.id
                )
                logging.info(
                    f"@{member.user.username} is member of chat_id={authorized_chat_id}"
                )
                await self.notify_chat(authorized_chat_id, message, message_type)
            except telegram.error.BadRequest as error:
                self.message = f"Member not found in chat_id={authorized_chat_id}"
