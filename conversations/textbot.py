import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    ConversationHandler,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from telegram.constants import ParseMode
from conversations.base import BaseConversation
from services.bot import BotAuthorizationService
from utils.botconfig import BotConfig


class TextbotConversation(BaseConversation):

    CHAT_SELECTION, TYPE_MESSAGE = range(2)

    def __init__(self, botconfig: BotConfig, name: str, *args, **kwargs):
        super().__init__(
            botconfig,
            name,
            [CommandHandler(name, self.start)],
            {
                self.CHAT_SELECTION: [
                    MessageHandler(
                        filters.Regex(f"[\w\s\d\W.-_]+"), self.get_chat_destination
                    )
                ],
                self.TYPE_MESSAGE: [
                    MessageHandler(
                        filters.Regex(f"[\w\s\d\W.-_\d]*"), self.get_message_to_send
                    )
                ]
            },
            [
                CommandHandler("cancel", self.cancel),
                MessageHandler(filters.Regex("^(Cancel)$"), self.cancel),
            ],
        )

    def __is_direct_chat_with_bot(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> bool:
        return update.effective_chat.id == update.effective_user.id

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logging.info(f"{self.name} has started.")
        if not self.__is_direct_chat_with_bot(update, context):
            logging.error("Must be a private chat with bot")
            return ConversationHandler.END
        auth_service = BotAuthorizationService(self._botconfig, context)
        if not auth_service.is_user_in_conversation_restricted_to_groups(
            update.effective_user.id, self.name
        ):
            logging.error(
                f"{update.effective_user.id} does not belong to the required restricted group."
            )
            return ConversationHandler.END
        user_authorized_chats = await auth_service.is_user_member_of_authorized_chats(
            update.effective_user.id
        )
        logging.info(f"User chats fetched: {user_authorized_chats}")
        context.user_data["chats"] = dict()
        for chat_id in user_authorized_chats:
            chat_name = (await context.bot.get_chat(chat_id)).effective_name
            context.user_data["chats"][chat_name] = chat_id

        keyboard = ReplyKeyboardMarkup([list(context.user_data["chats"].keys())])
        await update.message.reply_text(
            "Choose the chat you want to text",
            reply_markup=keyboard,
        )
        return self.CHAT_SELECTION

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Cancels and ends the conversation."""
        logging.info(f"{self.name} is cancelled.")
        return ConversationHandler.END

    async def get_chat_destination(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Cancels and ends the conversation."""
        logging.info(f"Get chat destination")
        logging.info(f"Chat: {context.user_data["chats"][update.effective_message.text]}")
        context.user_data["chat_destination"] = context.user_data["chats"][update.effective_message.text]
        await update.message.reply_text("What is the message you want to send ?",reply_markup=ReplyKeyboardRemove())
        return self.TYPE_MESSAGE

    async def get_message_to_send(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Cancels and ends the conversation."""
        logging.info(f"Get message to send")
        message_to_send = update.effective_message.text
        logging.info(f"Message to send: {message_to_send}")
        await update.message.reply_text("Ok, I will send it now.",reply_markup=ReplyKeyboardRemove())
        await context.bot.send_message(context.user_data["chat_destination"],message_to_send)
        return ConversationHandler.END
