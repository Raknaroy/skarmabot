from telegram.ext import Updater
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

if __name__ == "__main__":
    updater = Updater(token='TOKEN', use_context=True)
    dispatcher = updater.dispatcher

    updater.start_polling()

