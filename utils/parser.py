import re
import logging


class PropertyParser:
    """
    Pattern to retrieve property within bot.json
    A property is define in-between these marks '${}'
    """
    PROPERTY_PATTERN = r"\${?([\.\w]+)}?"

    def __init__(self, botconfig: dict) -> None:
        self.botconfig = botconfig
        self.properties = botconfig["properties"]
        self.chats = botconfig["chats"]

    def retrieve_property_from_variable(self, match_obj: re.Match) -> str:
        """Callback to remove variable tokens '${}' to get property
        and replace it by its value located in botconfig

        Args:
            match_obj (re.Match): property variable matched

        Returns:
            str: property's value
        """
        property = re.sub(r"[\$\{\}]", "", match_obj.group(0))
        logging.debug(f"Property retrieved: {property}")
        property_tokens = property.split(".")
        property_to_lookup = property_tokens.pop(0)
        bot_property = self.botconfig[property_to_lookup]
        for key in property_tokens:
            bot_property = bot_property[key]
        logging.debug(f"Properties obtained: {bot_property}")
        return bot_property

    def parse(self, message: str) -> str:
        """Parse all properties variable into their value

        Args:
            message (str): message to parse

        Returns:
            str: parsed message
        """
        return re.sub(
            self.PROPERTY_PATTERN, self.retrieve_property_from_variable, message
        )
