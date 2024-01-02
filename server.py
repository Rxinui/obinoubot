import logging
from commands import commands
from telegram.ext import ApplicationBuilder

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

if __name__ == "__main__":
    with open("token") as token_fp:
        TOKEN_BOT = token_fp.read()
        application = ApplicationBuilder().token(TOKEN_BOT).build()

        for command in commands:
            application.add_handler(command.handler)
            logging.info(f"main: add handler {command.command_name}")

        application.run_polling()
