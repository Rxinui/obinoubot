from utils.botconfig import BotConfig
from .help import HelpCommand
from .base import BaseCommand, BaseMessageCommand
from .conversations.newpr import NewPrConversation


def get_command_by_classname(command_classname: str) -> BaseCommand:
    print("DEBUG:get_command_by_classname:", globals()[command_classname])
    return globals().get(command_classname)
