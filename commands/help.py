import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from .base import BaseMessageCommand


class HelpCommand(BaseMessageCommand):
    def __init__(self, botconfig: dict):
        super().__init__(
            botconfig,
            name="help",
            message=self.__generate_help(botconfig),
            message_type="MARKDOWN",
        )

    def __generate_deprecated(self, is_deprecated: bool) -> str:
        return "\[Deprecated\]" if is_deprecated else ""

    def __generate_help(self, botconfig: dict) -> str:
        cmd_descriptions = []
        for cmd_name, cmd_info in botconfig["commands"].items():
            cmd_descriptions.append(f"/{cmd_name} \- {self.__generate_deprecated(cmd_info.get("deprecated"))} {cmd_info['description']}")
        return f"Les commandes du bot:\n\n{"\n".join(cmd_descriptions)}"
        
