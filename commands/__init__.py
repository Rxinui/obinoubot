from .pr import PrCommand
from .classement import ClassementCommand
from .newmu import NewMuCommand


def get_commands(botconfig: dict) -> set:
    return {PrCommand(botconfig), ClassementCommand(botconfig), NewMuCommand(botconfig)}
