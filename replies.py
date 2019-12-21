from telegram import InlineKeyboardButton, InlineKeyboardMarkup

greeting_text = """
<b>Welcome!</b>\n
This bot allows you to use crypting algorithms\n
Author                  <a href="tg://user?id=brebiv">@brebiv</a>
"""
help_text = """\
With this bot you can use popular crypting algorithms to provide secure of your data.
Sounds hard? Don't worry I'll tell how to use it ;)
"""
more_help_text = """\
More help text
"""

def greeting(self, update, context):
    kb = [[InlineKeyboardButton("Crypt!", callback_data="crypt")],
                [InlineKeyboardButton("Help", callback_data="help")]]
    kb_markup = InlineKeyboardMarkup(kb)
    self.greeting_m = context.bot.send_message(
            update.message.chat.id,
            greeting_text,
            parse_mode="HTML",
            reply_markup = kb_markup)

def help(self, update, context, callback):
    kb = [[InlineKeyboardButton("Crypt!", callback_data="crypt")],
            [InlineKeyboardButton("About algorithms", callback_data="more_help")]]
    kb_markup = InlineKeyboardMarkup(kb)
    try:
        context.bot.delete_message(callback.message.chat.id, self.greeting_m.message_id)
        del self.greeting_m
    except:
        print("NO MESSAGE TO DELETE")
    self.help_m = context.bot.send_message(callback.message.chat.id, help_text,
                                                reply_markup=kb_markup)

def more_help(self, update, context, callback):
    kb = [[InlineKeyboardButton("Crypt!", callback_data="crypt")]]
    kb_markup = InlineKeyboardMarkup(kb)
    if self.help_m:
        context.bot.delete_message(callback.message.chat.id, self.help_m.message_id)
        del self.help_m
    self.more_help_m = context.bot.send_message(callback.message.chat.id, more_help_text)

def crypt(self, update, context, callback):
    if self.help_m:
        context.bot.delete_message(callback.message.chat.id, self.help_m.message_id)
        del self.help_m
    elif self.greeting_m:
        context.bot.delete_message(callback.message.chat.id, self.greeting_m.message_id)
        del self.greeting_m
    self.choose_m = context.bot.send_message(callback.message.chat.id, "Crypting")

