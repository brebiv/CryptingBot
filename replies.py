from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def greeting(self, update, context):
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

def help(self, update, context, callback):
    kb = [[InlineKeyboardButton("Crypt!", callback_data="crypt")]]
    kb_markup = InlineKeyboardMarkup(kb)
    try:
        context.bot.delete_message(callback.message.chat.id, self.greeting_m.message_id)
        del self.greeting_m
    except:
        print("NO MESSAGE TO DELETE")
    self.help_m = context.bot.send_message(callback.message.chat.id, self.help_m,
                                                reply_markup=kb_markup)

def crypt(self, update, context, callback):
    if self.help_m:
        context.bot.delete_message(callback.message.chat.id, self.help_m.message_id)
        del self.help_m
    elif self.greeting_m:
        context.bot.delete_message(callback.message.chat.id, self.greeting_m.message_id)
        del self.greeting_m
    self.choose_m = context.bot.send_message(callback.message.chat.id, "Crypting")

