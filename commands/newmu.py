import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from .base import BaseCommand
from services import NewPrService


class NewMuCommand(BaseCommand):
    def __init__(self, botconfig: dict) -> None:
        super().__init__(botconfig, filename=__file__)

    # async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     logging.info(f"test: {context.args} | {update.message.text}")
    #     # TODO check value is number
    #     mu = float(context.args.pop(0))
    #     response = NewPrService.submit_new_mu(mu)
    #     if response.status_code == 200:
    #         text_to_send = f"@{update.message.from_user.username} a un nouveau PR *Muscle up*: {mu}kg"
    #     if response.status_code == 400:
    #         text_to_send = f"*Erreur: contacter l'admin.*"
    #     logging.info(text_to_send)
    #     await context.bot.send_message(
    #         chat_id=update.effective_chat.id,
    #         text=text_to_send,
    #         parse_mode=ParseMode.MARKDOWN,
    #     )
    #     logging.info(f"{self.command_name} has been triggered")
    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logging.info(f"test: {context.args} | {update.message.text}")
        
