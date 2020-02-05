from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import run_async
from telegram.ext import ConversationHandler
from telegram.error import BadRequest
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import hashlib
import time
import os

"""
Some stuff for user
"""

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

def greeting(self, update, context):
    kb = [[InlineKeyboardButton("Crypt!", callback_data="go")],
                [InlineKeyboardButton("Help", callback_data="help")]]
    kb_markup = InlineKeyboardMarkup(kb)
    self.greeting_m = context.bot.send_message(
            update.message.chat.id,
            greeting_text,
            parse_mode="HTML",
            reply_markup = kb_markup)

def help(self, update, context, callback):
    kb = [[InlineKeyboardButton("Crypt!", callback_data="go")],
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
    kb = [[InlineKeyboardButton("Crypt!", callback_data="go")]]
    kb_markup = InlineKeyboardMarkup(kb)
    if self.help_m:
        context.bot.delete_message(callback.message.chat.id, self.help_m.message_id)
        del self.help_m
    self.more_help_m = context.bot.send_message(callback.message.chat.id, more_help_text)


"""
Hashing conversation functions
"""

# states
CHOOSE_ALGORITHM, CHOOSE_VERSION, GET, HASH = range(4)

def generate_regex():
    regex = ""
    for i in hashing_algorithms:
        for j in hashing_algorithms[i]:
            regex += "|%s" % (j)
    return '^('+ regex +')$'

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
    return HASH

def hash(update, context):
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

"""
Encrypting functions
"""

CHOOSE_METHOD, KEY, GET, ENCRYPT = range(4)


def write_key(key):
    with open("key.key", 'wb') as file:
        file.write(key)

def load_key(id):
    with open(f"{id}.key", 'rb') as file:
        key = file.read()
    return key

def encrypt(data, key):
    f = Fernet(key)
    if type(data) == str:
        data = data.encode()
    encrypted = f.encrypt(data)
    #with open('1.data', 'wb') as file:
    #    file.write(encrypted)
    return encrypted

def decrypt(encrypted, key):
    f = Fernet(key)
    decrypted = f.decrypt(encrypted)
    return decrypted


def choose_method(update, context):
    text = \
"""
We will are using symmetric encryption, which means the same key we used to encrypt data, is also usable for decryption.\n
We are using AES-cbc\n
How to encrypt/decrypt?\n
With keyfile (safe):\n
You will recive keyfile wich you can use to (en/de)crypt your file, no one can access your file without keyfile.
But if you think you can lose your file, then you can use passphrase.\n
With passphrase (not safe):\n
In that case your file or message will be encrypted with your passphrase, it is like usual password, but for file.\n
What key would you like to use?
"""
    kb = [["File"], ["Passphrase"]]
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup(kb, one_time_keyboard=True))
    return KEY

def create_key(update, context):
    print("Create key")
    method = update.message.text
    context.user_data['method'] = method
    if method == "File":
        key = Fernet.generate_key()
        write_key(key)
        context.bot.send_document(update.message.chat.id, open('key.key','rb'), filename="yourkey.key")
        context.user_data['key'] = key
        update.message.reply_text("Your keyfile generated, send something to continue")
    else:
        update.message.reply_text("Send your passphrase")
    return GET

def get_data_to_encrypt(update, context):
    passphrase = update.message.text.encode()
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(passphrase))
    context.user_data['key'] = key
    print("Get file")
    update.message.reply_text("Getting file")
    return ENCRYPT

def crypt(update, context):
    print("Crypt")
    method = context.user_data['method']
    key = context.user_data['key']
    with open('key.txt', 'wb') as f:
        f.write(key)
    #file = context.bot.getFile(update.message.document.file_id)
    #data = file.download_as_bytearray()
    if method == "File":
        encrypted = encrypt(update.message.text, key)
        decrypted = decrypt(encrypted, key)
    else:
        encrypted = encrypt(update.message.text, key)
        with open('2.txt', 'wb') as f:
            f.write(encrypted)
        decrypted = decrypt(encrypted, key)
    text = f"Encrypted - {encrypted.decode('utf-8')}\nDecrpypted - {decrypted.decode('utf-8')}"
    #update.message.reply_text(encrypted.decode())
    update.message.reply_text(text)
    update.message.reply_text("Done!")
    return ConversationHandler.END

"""
Decryption functions
"""
CHOOSE_METHOD, GET_KEY, GET_FILE, DECRYPT = range(4)

def choose_key_type(update, context):
    update.message.reply_text("Choose key to decrypt")
    return GET_KEY

def get_key(update, context):
    update.message.reply_text("Getting key")
    return GET_FILE

def get_data_to_decrypt(update, context):
    update.message.reply_text("Getting data to decrypt")
    return DECRYPT

def _decrypt(update, context):
    update.message.reply_text("Decrypting")
    return ConversationHandler.END

def close(self, update, context):
    return ConversationHandler.END