from dotwiz import DotWiz
from pathlib import Path
import json


class BotConfig(DotWiz):
    def __init__(self, botconfig_file: str) -> None:
        botconfig_file = Path(botconfig_file)
        with open(str(botconfig_file)) as fp:
            super().__init__(json.load(fp))
