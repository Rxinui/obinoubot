from utils.botconfig import BotConfig
from .newmu import NewMuCommand
from .help import HelpCommand
from .generator import MessageCommandGenerator


def get_commands(botconfig: BotConfig) -> set:
    commands = MessageCommandGenerator.generate(botconfig)
    commands.append(HelpCommand(botconfig))
    return commands
