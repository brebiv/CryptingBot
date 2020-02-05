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

    # conversation states
    CHOOSE_ALGORITHM, CHOOSE_VERSION, GET, HASH = range(4)
    CHOOSE_METHOD, KEY, GET, ENCRYPT = range(4)
    CHOOSE_METHOD, GET_KEY, GET_FILE, DECRYPT = range(4)

    reg = replies.generate_regex()

    def main(self):
        hash_conv = ConversationHandler\
        (
                entry_points=[CommandHandler("hash", replies.choose_algorithm)],
                states={
                    self.CHOOSE_VERSION: [MessageHandler(Filters.regex('^(SHA|md)$'), replies.choose_version)],
                    self.GET: [MessageHandler(Filters.regex('^(%s)$'%(self.reg)), replies.get_data)],
                    self.HASH: [MessageHandler(Filters.text | Filters.document, replies.hash)]
                    },
                fallbacks=[MessageHandler(Filters.regex('^Close$'), replies.close)]
        )

        encrypt_conv = ConversationHandler\
        (
            entry_points=[CommandHandler("encrypt", replies.choose_method)],
            states={
                self.KEY: [MessageHandler(Filters.text, replies.create_key)],
                self.GET: [MessageHandler(Filters.text, replies.get_data_to_encrypt)],
                self.ENCRYPT: [MessageHandler(Filters.text | Filters.document, replies.crypt)]
            },
            fallbacks=[MessageHandler(Filters.regex("^Close$"), replies.close)]
        )

        decrypt_conv = ConversationHandler\
        (
            entry_points=[CommandHandler("decrypt", replies.choose_key_type)],
            states={
                self.GET_KEY: [MessageHandler(Filters.text, replies.get_data_to_decrypt)],
                self.GET_FILE: [MessageHandler(Filters.text, replies._decrypt)],
                self.DECRYPT: [MessageHandler(Filters.text, replies._decrypt)]
            },
            fallbacks=[MessageHandler(Filters.regex("^Close%"), replies.close)]
        )

        self.dp.add_handler(CommandHandler("start", self.start_handler))
        self.dp.add_handler(CallbackQueryHandler(self.callback_handler))
        self.dp.add_handler(hash_conv)
        self.dp.add_handler(encrypt_conv)
        self.dp.add_handler(decrypt_conv)

        self.updater.start_polling()
    
    def start_handler(self, update, context):
        replies.greeting(self, update, context)

    def callback_handler(self, update, context):
        callback = update.callback_query
        if callback.data == "help":
            replies.help(self, update, context, callback)
        elif callback.data == "more_help":
            replies.more_help(self, update, context, callback)
        elif callback.data == "go":
            update.callback_query.message.reply_text("Use /encrypt to encrypt\n"\
                                                        "Use /decrypt to decrypt\n"
                                                        "Use /hash to hash")
