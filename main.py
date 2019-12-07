#!/usr/bin/env python

import os
from os.path import join, dirname
from dotenv import load_dotenv

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Load Environments
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get("API_TOKEN")
GROUP_CHAT_ID = os.environ.get("GROUP_CHAT_ID")
REGISTERED_USERS = os.environ.get("REGISTERED_USERS")

# Enable logging
logging.basicConfig(filename='logs', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Utilities functions
def is_registered_user(username):
    for user in REGISTERED_USERS.split(','):
        if username == user:
            return True
    return False

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    logger.info('GROUP NAME: %s\nGROUP ID: %s', update.effective_chat.title, update.effective_chat.id)
    update.message.reply_text('The Admiral General Aladeen at your service. Death to the west.')

def help(update, context):
    """Send a message when the command /help is issued."""
    logger.info('UPDATER DICT: %s', update)
    update.message.reply_text('You don\'t get to ask for help')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def send_to_a_group(update, context):
    logger.info('UPDATE DICT: %s', update)

    if is_registered_user(update.effective_user.username):
        context.bot.send_message(GROUP_CHAT_ID, text=update.message.text)
    else:
        update.message.reply_text('You are not a registered user')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.text, send_to_a_group))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    logger.info("National Stability Bot Started!")
    main()
    
