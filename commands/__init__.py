from .pr import PrCommand
from .classement import ClassementCommand
from .newmu import NewMuCommand

commands = {
    PrCommand(),
    ClassementCommand(),
    NewMuCommand()
}