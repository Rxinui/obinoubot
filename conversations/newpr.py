from datetime import timedelta
from typing import Any, Dict, List
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram._utils.defaultvalue import DEFAULT_TRUE
from telegram.ext import ConversationHandler, ContextTypes, CommandHandler, MessageHandler, filters
from telegram.constants import ParseMode
import logging

class NewPrConversation(ConversationHandler):

  ENTER_PR, REGISTER_PR, SUBMIT = range(3)

  MU = "MU"
  PULL = "Pull"
  DIPS = "Dips"
  SQUAT = "Squat"

  def __init__(self):
    super().__init__(self.entry_points, self.states, self.fallbacks)
    self.reply_keyboard = ReplyKeyboardMarkup([[self.MU,self.PULL,self.DIPS,self.SQUAT],["Cancel","Submit"]], one_time_keyboard=True, input_field_placeholder="MU / Pull / Dips / Squat")
  
  @property
  def entry_points(self):
    return [CommandHandler("newpr",self.start)]
  
  @property
  def states(self):
    return {
      self.ENTER_PR: [MessageHandler(filters.Regex("^(MU|Pull|Dips|Squat)$"),self.enter_pr),MessageHandler(filters.Regex("^(Submit)$"),self.submit)],
      self.REGISTER_PR: [MessageHandler(filters.Regex("^[0-9\.]+$"),self.register_pr)]
    }
  
  @property
  def fallbacks(self):
    return [CommandHandler("cancel",self.cancel)]
  
  @staticmethod
  def __stringify_prs(prs: dict[str]) -> str:
    return f"MU: {prs.get(NewPrConversation.MU,"")}\n" \
    f"Pull: {prs.get(NewPrConversation.PULL,"")}\n" \
    f"Dips: {prs.get(NewPrConversation.DIPS,"")}\n" \
    f"Squat: {prs.get(NewPrConversation.SQUAT,"")}\n" 
  
  async def start(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"{update.effective_user} started {self.__class__.__name__}")
    text_explaination = "Use below keyboard to select which lift you want to register your PR.\n" \
    "Please note that *decimal number must be written using* `.` and not `,`\n" \
    "*This is a correct PR value*: `92.5`\n" \
    "This is not a correct PR value: `190,25`"
    await update.message.reply_text(text_explaination,parse_mode=ParseMode.MARKDOWN,reply_markup=self.reply_keyboard)
    return self.ENTER_PR

  async def enter_pr(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["selected"] = update.message.text
    text = f"*Enter PR for {context.user_data["selected"]}*"
    await update.message.reply_text(text,parse_mode=ParseMode.MARKDOWN,reply_markup=ReplyKeyboardRemove()
    )
    return self.REGISTER_PR

  async def register_pr(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[context.user_data["selected"]] = float(update.message.text)
    text = f"PRs registered:\n" \
    f"{'-'*20}\n" \
    f"{self.__stringify_prs(context.user_data)}" \
    f"{'-'*20}\n" \
    f"Use below keyboard to :\n- Add or update a PR\n- Submit the PRs you registered"
    await update.message.reply_text(
      text,reply_markup=self.reply_keyboard
    )
    return self.ENTER_PR

  async def submit(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
    del context.user_data["selected"]
    await update.message.reply_text(
      f"@{update.effective_user.username} your PRs {context.user_data} have been submitted",reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()
    return ConversationHandler.END
  
  async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Bye!", reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()
    return ConversationHandler.END


  

