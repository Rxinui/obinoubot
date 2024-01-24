class UnauthorizedChatError(Exception):
    """Exception raised when a message is send to an unauthorized chat.
    """
    def __init__(self, chat_id: str | int) -> None:
        self.chat_id = chat_id
        self.message = f"Chat id={chat_id} is not authorized by the bot."
        super().__init__(self.message)
