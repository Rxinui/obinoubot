import logging
from typing import List, Dict, Any
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from .base import BaseMessageCommand
from utils import BotConfig

class MessageCommandGenerator:

    @classmethod
    def generate(cls, botconfig: BotConfig) -> List[__name__]:
        """Fetch all commands that are instance of MessageCommandGenerator

        Args:
            botconfig (dict): bot config

        Returns:
            List[Dict[str, Any]]: commands message
        """
        commands = []
        for cmd_name, cmd_info in botconfig.commands.items():
            if cmd_info["instance_of"] == BaseMessageCommand.__name__:
                instance = BaseMessageCommand(
                    botconfig,
                    cmd_name,
                    **cmd_info["args"],
                )
                commands.append(instance)
        return commands
