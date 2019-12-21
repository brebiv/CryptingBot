from telegram.ext import Updater, Dispatcher
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import run_async
from config import *
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
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CallbackQueryHandler(self.callback_handler))

        self.updater.start_polling()
    
    def start(self, update, context):
        kb = [[InlineKeyboardButton("Crypt!", callback_data="crypt")],
                [InlineKeyboardButton("Help", callback_data="help")]]
        kb_markup = InlineKeyboardMarkup(kb)
        self.greeting_m = context.bot.send_message(
                update.message.chat.id,
                '<b>WELCOME!</b>\n'\
                'This bot allows you to use crypting algorithm\n'
                'Author                  <a href="tg://user?id=brebiv">@brebiv</a>',
                parse_mode="HTML",
                reply_markup = kb_markup)

    def callback_handler(self, update, context):
        callback = update.callback_query
        if callback.data == "help":
            kb = [[InlineKeyboardButton("Crypt!", callback_data="crypt")]]
            kb_markup = InlineKeyboardMarkup(kb)
            try:
                context.bot.delete_message(callback.message.chat.id, self.greeting_m.message_id)
                del self.greeting_m
            except:
                print("NO MESSAGE TO DELETE")
            self.help_m = context.bot.send_message(callback.message.chat.id, self.help_m,
                                                      reply_markup=kb_markup)
        elif callback.data == "crypt":
            if self.help_m:
                context.bot.delete_message(callback.message.chat.id, self.help_m.message_id)
                del self.help_m
            elif self.greeting_m:
                context.bot.delete_message(callback.message.chat.id, self.greeting_m.message_id)
                del self.greeting_m
            self.choose_m = context.bot.send_message(callback.message.chat.id, "Crypting")
