from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import run_async
from telegram.ext import ConversationHandler
from telegram.error import BadRequest
import hashlib
import time

greeting_text = \
"""
<b>Welcome!</b>\n
This bot allows you to use crypting algorithms\n
Now available popular hashing algorithms
Crypt algorithms <b>SOON</b>\n
Author                  <a href="tg://user?id=brebiv">@brebiv</a>
"""
help_text = \
"""
With this bot you can use popular crypting algorithms to provide secure of your data.
For now only hashing algorithms available. Crypt algorithms like AES will be able soon!
"""
more_help_text = \
"""
Hashing:
https://en.wikipedia.org/wiki/Hash_function
"""
hashing_algorithms = {
        "SHA" : ["sha1", "sha224", "sha256", "sha384", "sha512"],
        "md" : ["md4","md5"]}

def generate_regex():
    regex = ""
    for i in hashing_algorithms:
        for j in hashing_algorithms[i]:
            regex += "|%s" % (j)
    return '^('+ regex +')$'

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

CHOOSE_ALGORITHM, CHOOSE_VERSION, GET, CRYPT = range(4)

def choose_algorithm(update, context):
    kb = []
    for i in hashing_algorithms:
        kb.append([KeyboardButton(i)])
    update.message.reply_text("Choose algorithm\n"
                              "You can use /close to stop",
                                reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True))
    return CHOOSE_VERSION

def choose_version(update, context):
    algorithm = update.message.text
    context.user_data["algorithm"] = algorithm
    kb = []
    for i in hashing_algorithms[algorithm]:
        kb.append([KeyboardButton(i)])
    update.message.reply_text("Algorithm: <b>%s</b>\n"
                              "Version:   <b>---</b>\n" % (algorithm),
                              parse_mode="HTML")
    update.message.reply_text("Choose version for %s\n"
                              "You can use /close to stop" % (algorithm),
                                reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True))
    return GET

def get_data(update, context):
    version = update.message.text
    context.user_data["version"] = version
    algorithm = context.user_data["algorithm"]
    update.message.reply_text("Algorithm: <b>%s</b>\n"
                              "Version:   <b>%s</b>\n" % (algorithm, version),
                              parse_mode="HTML")
    update.message.reply_text("Send me text message if you want to hash text"
                              " or send me any other file by sending it like a file\n"
                              "You can use /close to stop\n\n"
                              "Send files that is <b>less then 20 mb</b>. Because it is Telegram restriction",
                              parse_mode="HTML")
    update.message.reply_text("Send me what you want to hash with <b>%s</b>\n" % (version),
                              parse_mode="HTML")
    return CRYPT

def crypt(update, context):
    start = time.time()

    message = update.message
    data = None
    version = context.user_data["version"]
    hashed_data = None

    if message.document:
        # print(f"\n\n\n {file.file_size} \n\n\n")
        try:
            file = context.bot.getFile(update.message.document.file_id)
        except BadRequest:
            update.message.reply_text("File is too <b>BIG</b>\n"
                                      "File should be less then <b>20 mb</b>. It's <i>not mine</i>, "
                                      "it's Telegram restriction.\n"
                                      "Please send file with correct size or text",
                                      parse_mode="HTML")
            return CRYPT
        except:
            update.message.reply_text("Unknown error happened ¯\_(ツ)_/¯")
            return ConversationHandler.END
        else:
            update.message.reply_text("Please wait, it may take some time\n"
                                      "Depends on your file size.......")
            data = file.download_as_bytearray()
            hashed_data = hashlib.new(version, data).hexdigest()
    else:
        data = message.text
        hashed_data = hashlib.new(version, str.encode(data)).hexdigest()

    update.message.reply_text("Result! It was hashed with %s" %(version))
    update.message.reply_text("Here it is:\n%s" %hashed_data)
    update.message.reply_text("Done in %.2f sec" % (time.time()-start))
    return ConversationHandler.END

def close(self, update, context):
    return ConversationHandler.END