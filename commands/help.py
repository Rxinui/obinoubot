import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from commands.base import BaseMessageCommand
from utils.botconfig import BotConfig

class HelpCommand(BaseMessageCommand):
    def __init__(self, botconfig: BotConfig, *args, **kwargs):
        super().__init__(
            botconfig,
            name="help",
            message=self.__generate_help(botconfig),
            message_type="MARKDOWN",
        )

    def __generate_deprecated(self, is_deprecated: bool) -> str:
        return "(Deprecated)" if is_deprecated else ""

    def __generate_help(self, botconfig: BotConfig) -> str:
        cmd_descriptions = []
        for cmd_name, cmd_info in botconfig.conversations.items():
            cmd_descriptions.append(f"/{cmd_name} - {self.__generate_deprecated(cmd_info.get("deprecated"))} {cmd_info['description']}")
        for cmd_name, cmd_info in botconfig.commands.items():
            cmd_descriptions.append(f"/{cmd_name} - {self.__generate_deprecated(cmd_info.get("deprecated"))} {cmd_info['description']}")
        
        return f"Commands available are:\n\n{"\n".join(cmd_descriptions)}"
        
