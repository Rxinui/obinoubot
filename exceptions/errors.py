class UnauthorizedChatError(Exception):
    """Exception raised when a message is send to an unauthorized chat."""

    def __init__(self, chat_id: str | int) -> None:
        self.chat_id = chat_id
        self.message = f"chat_id={chat_id} is not authorized by the bot."
        super().__init__(self.message)


class UnauthorizedMemberError(Exception):
    """Exception raised when a user is not a member of an authorized chat."""

    def __init__(self, chat_id, user_id) -> None:
        self.chat_id = chat_id
        self.user_id = user_id
        self.message = f"user_id={user_id} is not recognized as an authorized member of chat_id={chat_id}."
        super().__init__(self.message)


class CommandNotAllowedError(Exception):
    """Exception raised when a command is triggered from an authorized chat that is not in the whitelist 'allowed_for'."""

    def __init__(self, command: str, chat_id: str | int) -> None:
        self.chat_id = chat_id
        self.command = command
        self.message = f"command={command} is not allowed in chat_id={chat_id}"
        super().__init__(self.message)
