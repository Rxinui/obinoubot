import logging
from typing import List, Dict, Any
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from .base import BaseCommand


class MessageCommandGenerator:
    @classmethod
    def __load_commands(cls, botconfig: dict) -> List[Dict[str, Any]]:
        """Fetch all commands that are instance of MessageCommandGenerator

        Args:
            botconfig (dict): bot config

        Returns:
            List[Dict[str, Any]]: commands message
        """
        return [
            
        ]
    
    @classmethod
    async def execute(cls, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        logging.info(f"{self.command_name} has been triggered")
    
    @classmethod
    def generate(cls,botconfig: dict) -> List[__name__]:
        commands = []
        for cmd_name, cmd_info in botconfig["commands"].items():
            if cmd_info["instance_of"] == cls.__name__:
                i = BaseMessageCommand(botconfig,cmd_name)
                i.execute = cls.execute

                commands.append()
        return
