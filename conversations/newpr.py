import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ConversationHandler, ContextTypes, CommandHandler, MessageHandler, filters
from telegram.constants import ParseMode

from conversations.base import BaseConversation
from services.bot import BotAuthorizationService, BotMessageService
from services.newpr import NewPrService
from utils.botconfig import BotConfig

class NewPrConversation(BaseConversation):

  ENTER_CATEGORY, ENTER_PR, REGISTER_PR, SUBMIT, NOTIFY_CHATS = range(5)

  MU = "MU"
  PULL = "Pull"
  DIPS = "Dips"
  SQUAT = "Squat"

  CATEGORIES = NewPrService.categories()

  def __init__(self, botconfig: BotConfig, name: str, notify_chats: list[str|int] = [], *args, **kwargs):
    super().__init__(
      botconfig, 
      name, 
      entry_points=[CommandHandler(name,self.start)], 
      states={
        self.ENTER_CATEGORY: [MessageHandler(filters.Regex(f'^({"|".join(self.CATEGORIES)})$'),self.enter_category)],
        self.ENTER_PR: [MessageHandler(filters.Regex(f"^(MU|Pull|Dips|Squat)$"),self.enter_pr),MessageHandler(filters.Regex("^(Submit)$"),self.submit)],
        self.REGISTER_PR: [MessageHandler(filters.Regex("^[0-9.]+$"),self.register_pr),MessageHandler(filters.Regex("^(Submit)$"),self.register_pr)],
      }, 
      fallbacks=[CommandHandler("cancel",self.cancel),MessageHandler(filters.Regex("^(Cancel)$"),self.cancel)]
    )
    self.reply_lift_keyboard = ReplyKeyboardMarkup([[self.MU,self.PULL,self.DIPS,self.SQUAT],["Cancel","Submit"]], one_time_keyboard=True, input_field_placeholder="Enter your new PRs using below keyboard")
    self.reply_category_keyboard = ReplyKeyboardMarkup([self.CATEGORIES[:4],self.CATEGORIES[4:7],self.CATEGORIES[7:],["Cancel"]], one_time_keyboard=True, input_field_placeholder="Enter your new PRs using below keyboard")
    
    self._notify_chats = notify_chats

  @property
  def handler(self) -> ConversationHandler:
    return super().handler

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
    # ERROR CASE 1 : user start a conversation inside a group chat
    if not self.__is_direct_chat_with_bot(update,context):
      logging.error(f"Conversation is started in a group {update.effective_chat}")
      await update.message.reply_text(f"/{self.name} must be called in a private chat with @{context.bot.username}",parse_mode=ParseMode.HTML,reply_markup=ReplyKeyboardRemove())
      return ConversationHandler.END
    # ERROR CASE 2 : user does not have a Telegram Username
    if not self.__user_has_username(update,context):
      logging.error(f"User {update.effective_user} must have a Telegram username to use /{self.name}")
      await update.message.reply_text(f"You must have a Telegram Username to use /{self.name}",parse_mode=ParseMode.MARKDOWN,reply_markup=ReplyKeyboardRemove())
      return ConversationHandler.END
    # ERROR CASE 3: user does not belong to any of authorized chats
    authorization_service = BotAuthorizationService(self._botconfig,context)
    context.user_data["user_chats"] = await authorization_service.is_user_member_of_authorized_chats(update.effective_user.id)
    if len(context.user_data["user_chats"]) == 0:
      logging.error(f"User {update.effective_user} must be a member to one of the authorized chats.")
      await update.message.reply_text(f"You are not authorized to use this command because you are not a member.",parse_mode=ParseMode.MARKDOWN,reply_markup=ReplyKeyboardRemove())
      return ConversationHandler.END
    text_to_send = "Tell me your weight class category using below keyboard"
    await update.message.reply_text(text_to_send,parse_mode=ParseMode.MARKDOWN,reply_markup=self.reply_category_keyboard)
    return self.ENTER_CATEGORY

  async def enter_category(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["category"] = update.message.text
    context.user_data["gender"] = NewPrService.guess_gender_from_category(context.user_data['category'])
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
    text = f"PRs registered in {context.user_data['gender']} {context.user_data['category']} category:\n" \
    f"{'-'*32}\n" \
    f"{self.__stringify_prs(context.user_data)}" \
    f"{'-'*32}\n" \
    f"Use below keyboard to :\n- Add or update a PR\n- Submit the PRs you registered"
    await update.message.reply_text(
      text,reply_markup=self.reply_lift_keyboard
    )
    return self.ENTER_PR

  async def submit(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not any([context.user_data.get(self.MU),context.user_data.get(self.PULL),context.user_data.get(self.DIPS),context.user_data.get(self.SQUAT)]):
      logging.warn("No PRs has been registered. Exit.")
      await update.message.reply_text(f"No PRs has been registered. Can't submit. Please use /{self.name} again.",reply_markup=ReplyKeyboardRemove(),parse_mode=ParseMode.HTML
      )
      return ConversationHandler.END
    success_links = ""
    error_links = ""
    text_to_send = ""
    success_text = f"I see you've gotten stronger @{update.effective_user.username}.\nYour PRs have been submitted and your rank is updated on:"
    error_text = f"Error when updating PRs on the following links:"
    for user_chat in context.user_data["user_chats"]:
      user_chat_key = self._botconfig.inverted_chats[user_chat]
      new_pr_service = NewPrService(self._botconfig.properties[user_chat_key].GFORM_PR_POST,self._botconfig.properties[user_chat_key].GFORM_PR_POST_ENTRY_USERNAME,self._botconfig.properties[user_chat_key].GFORM_PR_POST_ENTRY_CATEGORY,self._botconfig.properties[user_chat_key].GFORM_PR_POST_ENTRY_MU,self._botconfig.properties[user_chat_key].GFORM_PR_POST_ENTRY_PULL,self._botconfig.properties[user_chat_key].GFORM_PR_POST_ENTRY_DIPS,self._botconfig.properties[user_chat_key].GFORM_PR_POST_ENTRY_SQUAT)
      response = new_pr_service.new_pr(update.effective_user.username,context.user_data["category"],context.user_data.get(self.MU),context.user_data.get(self.PULL),context.user_data.get(self.DIPS),context.user_data.get(self.SQUAT)).submit()
      if response.status_code == 200:
        success_links += f"- [{user_chat_key}]({self._botconfig.properties[user_chat_key].GSHEET_RANKING})\n"
        logging.info(success_text)
      if response.status_code == 400:
        error_links += f"- [{user_chat_key}]({self._botconfig.properties[user_chat_key].GSHEET_RANKING})\n"
        logging.error(response.reason)
    if success_links:
      text_to_send += f"{success_text}\n{success_links}\n\n"
    if error_links:
      text_to_send += f"{error_text}\n{error_links}"
    await update.message.reply_text(
      self._parser.parse(text_to_send),reply_markup=ReplyKeyboardRemove(),parse_mode=ParseMode.MARKDOWN
    )
    self.teardown_user_data(update,context)
    await self.notify_group(update, context)
    return ConversationHandler.END

  def teardown_user_data(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
    del context.user_data["selected"]
    del context.user_data["gender"]
    del context.user_data["user_chats"]

  async def notify_group(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
    service = BotMessageService(self._botconfig,update,context)
    prs = '\n'.join([ f'{lift.capitalize()}: {pr}' for lift, pr in context.user_data.items() if pr])
    message = f"Be aware that @{update.effective_user.username} has new PRs folks !\n{prs}"
    await service.notify_authorized_chats_where_user_is_member(message)
    return context.user_data.clear()
  
  async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        f"No PR today I guess.. you are so weak.", reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()
    return ConversationHandler.END
