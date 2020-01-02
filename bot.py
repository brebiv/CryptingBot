from telegram.ext import Updater, Dispatcher
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, MessageHandler, 
                            Filters, ConversationHandler)
from config import *
import replies

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Bot:
    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Messages
    greeting_m = None               # Greeting message
    help_m = None                   # Simple help message
    more_help_m = None              # Advanced help message
    choose_m = None                 # Choose algorithm message

    # states
    CHOOSE_ALGORITHM, CHOOSE_VERSION, GET, CRYPT = range(4)

    reg = replies.generate_regex()

    def main(self):
        crypt_conv = ConversationHandler\
        (
                entry_points=[CommandHandler("crypt", replies.choose_algorithm)],
                states={
                    self.CHOOSE_VERSION: [MessageHandler(Filters.regex('^(SHA|md)$'), replies.choose_version)],
                    self.GET: [MessageHandler(Filters.regex('^(%s)$'%(self.reg)), replies.get_data)],
                    self.CRYPT: [MessageHandler(Filters.text | Filters.document, replies.crypt)]
                    },
                fallbacks=[MessageHandler(Filters.regex('^Close$'), replies.close)]
        )

        self.dp.add_handler(CommandHandler("start", self.start_handler))
        self.dp.add_handler(CallbackQueryHandler(self.callback_handler))
        self.dp.add_handler(crypt_conv)

        self.updater.start_polling()
    
    def start_handler(self, update, context):
        replies.greeting(self, update, context)

    def callback_handler(self, update, context):
        callback = update.callback_query
        if callback.data == "help":
            replies.help(self, update, context, callback)
        elif callback.data == "more_help":
            replies.more_help(self, update, context, callback)
        elif callback.data == "crypt":
            update.callback_query.message.reply_text("Use /crypt to crypt")
