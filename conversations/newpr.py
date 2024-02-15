from datetime import timedelta
from typing import Any, Dict, List
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram._utils.defaultvalue import DEFAULT_TRUE
from telegram.ext import ConversationHandler, ContextTypes, CommandHandler, MessageHandler, filters
from telegram.constants import ParseMode
import logging

from utils.botconfig import BotConfig
from utils.parser import PropertyParser
from services import NewPrService

class NewPrConversation(ConversationHandler):

  ENTER_CATEGORY, ENTER_PR, REGISTER_PR, SUBMIT = range(4)

  MU = "MU"
  PULL = "Pull"
  DIPS = "Dips"
  SQUAT = "Squat"

  COMMAND_NAME = "newpr"

  def __init__(self, botconfig: BotConfig):
    super().__init__(self.entry_points, self.states, self.fallbacks)
    self._botconfig = botconfig
    self._parser = PropertyParser(botconfig)
    self.reply_lift_keyboard = ReplyKeyboardMarkup([[self.MU,self.PULL,self.DIPS,self.SQUAT],["Cancel","Submit"]], one_time_keyboard=True, input_field_placeholder="Enter your new PRs using below keyboard")
    self.reply_category_keyboard = ReplyKeyboardMarkup([NewPrService.CATEGORIES[:4],NewPrService.CATEGORIES[4:],["Cancel"]], one_time_keyboard=True, input_field_placeholder="Enter your new PRs using below keyboard")
  
  @property
  def entry_points(self):
    return [CommandHandler(self.COMMAND_NAME,self.start)]
  
  @property
  def states(self):
    return {
      self.ENTER_CATEGORY: [MessageHandler(filters.Regex(f'^({"|".join(NewPrService.CATEGORIES)})$'),self.enter_category)],
      self.ENTER_PR: [MessageHandler(filters.Regex(f"^(MU|Pull|Dips|Squat)$"),self.enter_pr),MessageHandler(filters.Regex("^(Submit)$"),self.submit)],
      self.REGISTER_PR: [MessageHandler(filters.Regex("^[0-9\.]+$"),self.register_pr)]
    }
  
  @property
  def fallbacks(self):
    return [CommandHandler("cancel",self.cancel),MessageHandler(filters.Regex("^(Cancel)$"),self.cancel)]
  
  @staticmethod
  def __stringify_prs(prs: dict[str]) -> str:
    return f"MU: {prs.get(NewPrConversation.MU,"")}\n" \
    f"Pull: {prs.get(NewPrConversation.PULL,"")}\n" \
    f"Dips: {prs.get(NewPrConversation.DIPS,"")}\n" \
    f"Squat: {prs.get(NewPrConversation.SQUAT,"")}\n" 
  
  def __is_direct_chat_with_bot(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    return update.effective_chat.id == update.effective_user.id

  def __user_has_username(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    return True if update.effective_user.username else False
  
  async def start(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"{update.effective_user} started {self.__class__.__name__}")
    if not self.__is_direct_chat_with_bot(update,context):
      logging.error(f"Conversation is started in a group {update.effective_chat}")
      await update.message.reply_text(f"/{self.COMMAND_NAME} *must be called in a private chat* with @{context.bot.username}",parse_mode=ParseMode.MARKDOWN,reply_markup=ReplyKeyboardRemove())
      return ConversationHandler.END
    if not self.__user_has_username(update,context):
      logging.error(f"User {update.effective_user} must have a Telegram username to use /{self.COMMAND_NAME}")
      await update.message.reply_text(f"You must have a Telegram Username to use /{self.COMMAND_NAME}",parse_mode=ParseMode.MARKDOWN,reply_markup=ReplyKeyboardRemove())
      return ConversationHandler.END
    text_to_send = "Tell me your weight class category using below keyboard"
    await update.message.reply_text(text_to_send,parse_mode=ParseMode.MARKDOWN,reply_markup=self.reply_category_keyboard)
    return self.ENTER_CATEGORY

  async def enter_category(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["category"] = update.message.text
    text_to_send = "Use below keyboard to select which lift you want to register your PR.\n" \
    "Please note that *decimal number must be written using* `.` and not `,`\n" \
    "_This is a correct PR value:_ `92.5`\n" \
    "_This is NOT a correct PR value:_ `190,25`"
    await update.message.reply_text(text_to_send,parse_mode=ParseMode.MARKDOWN,reply_markup=self.reply_lift_keyboard)
    return self.ENTER_PR

  async def enter_pr(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["selected"] = update.message.text
    text = f"What is your *{context.user_data["selected"]}* PR?"
    await update.message.reply_text(text,parse_mode=ParseMode.MARKDOWN,reply_markup=ReplyKeyboardRemove()
    )
    return self.REGISTER_PR

  async def register_pr(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[context.user_data["selected"]] = float(update.message.text)
    text = f"PRs registered in {context.user_data['category']} category:\n" \
    f"{'-'*30}\n" \
    f"{self.__stringify_prs(context.user_data)}" \
    f"{'-'*30}\n" \
    f"Use below keyboard to :\n- Add or update a PR\n- Submit the PRs you registered"
    await update.message.reply_text(
      text,reply_markup=self.reply_lift_keyboard
    )
    return self.ENTER_PR

  async def submit(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
    del context.user_data["selected"]
    service = NewPrService()
    response = service.submit_new_pr(user_id=update.effective_user.username,category=context.user_data["category"],mu=context.user_data.get(self.MU),pull=context.user_data.get(self.PULL),dips=context.user_data.get(self.DIPS),squat=context.user_data.get(self.SQUAT))
    if response.status_code == 200:
      text_to_send = "I see you've gotten stronger." \
        f"@{update.effective_user.username} your PRs have been submitted.\n" \
        "See your new rank here ${properties.GOOGLE_SHEET_CLASSEMENT}"
      logging.info(text_to_send)
    if response.status_code == 400:
      text_to_send = f"*Erreur: contacter l'admin.*"
      logging.error(text_to_send)
    await update.message.reply_text(
      self._parser.parse(text_to_send),reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()
    return ConversationHandler.END
  
  async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        f"No PR today I guess.. so weak.", reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()
    return ConversationHandler.END


  

