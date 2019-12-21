from telegram.ext import Updater, Dispatcher
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import run_async
from config import *
import replies
import hashlib

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
import time

class Bot:
    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher

    #Messages
    greeting_m = None

    help_m = None
    choose_m = None

    def main(self):
        self.dp.add_handler(CommandHandler("start", self.start_handler))
        self.dp.add_handler(CallbackQueryHandler(self.callback_handler))

        self.updater.start_polling()
    
    def start_handler(self, update, context):
        replies.greeting(self, update, context)

    def callback_handler(self, update, context):
        callback = update.callback_query
        if callback.data == "help":
            replies.help(self, update, context, callback)
        elif callback.data == "crypt":
            replies.crypt(self, update, context, callback)
