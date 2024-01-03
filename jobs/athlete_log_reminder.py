import logging
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from .base import BaseJob
from utils import Singleton

class AthleteLogReminderJob(BaseJob,metaclass=Singleton):

    __name__ = "AtheleLogReminderJob"
    
    async def __call__(self,context: ContextTypes.DEFAULT_TYPE):
        super().__call__(context)
        await context.bot.send_message(chat_id="-1001959905789", text="*N'oubliez pas de logger vos RIRs sur votre programmation*", parse_mode=ParseMode.MARKDOWN)

