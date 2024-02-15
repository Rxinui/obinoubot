from telegram import Update
from telegram.ext import ContextTypes
from commands.base import BaseCommand, BaseMessageCommand
from services import BotReplyService
from utils.botconfig import BotConfig
class MeCommand(BaseMessageCommand):

    def __init__(self, botconfig: BotConfig, name: str = None):
        super().__init__(botconfig, name,message_type="MARKDOWN_V2")

    async def execute(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs
    ):
        self.message = f"userid\={update.effective_user.id} username\={update.effective_user.username}"
        await super().execute(update,context)
    
