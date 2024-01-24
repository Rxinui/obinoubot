from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from exceptions import UnauthorizedChatError
from . import BotConfig

class BotReplyService:
    def __init__(
        self, botconfig: BotConfig, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        self.__botconfig = botconfig
        self.__update = update
        self.__context = context

    async def send_message(
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
        if not self.is_coming_from_authorized_chats(self.__update.effective_chat.id):
            raise UnauthorizedChatError(self.__update.effective_chat.id)
        await self.__context.bot.send_message(
            self.__update.effective_chat.id, text=message, parse_mode=message_type
        )

    def is_coming_from_authorized_chats(self, chat_id: str | int) -> bool:
        """Verify that the request issued to the bot is coming from an authorized chat.

        Args:
            chat_id (str | int): chat id where the request is issued

        Returns:
            bool: True if the chat is authorized else False
        """
        chat_id = str(chat_id)
        check = [
            chat_id == authorized_chat_id
            for authorized_chat_id in self.__botconfig.chats.values()
        ]
        return any(check)
