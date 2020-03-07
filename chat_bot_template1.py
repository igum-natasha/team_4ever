#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import logging

from setup import PROXY, TOKEN
from telegram import Bot, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
array=[]
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def analise(func):
    def inner(*args, **kwargs):
        update=argv[0]
        if update and hasattr(update, 'message') and hasattr(update,'effective_user'):
            array.append({
                "user":update.effective_user.first_name,
                "function":func.__name__,
                "message":update.message.text})
        return func(*args, **kwargs)
    return inner

@analise
def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'Привет, {update.effective_user.first_name}!')

@analise
def chat_help(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Введи команду /start для начала. ')

@analise
def echo(update: Update, context: CallbackContext):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning(f'Update {update} caused error {context.error}')


def history(update: Updater, context: CallbackContext):
    handle=open("history.txt","w")
    history=[]
    update.message.reply_text("There are not actions")
    if len(array)==0:
        handle.write("There are not actions")
        update.message.reply_text("There are not actions")
    elif len(array)>=5:
        handle.write("Last five actions are:")
        update.message.reply_text("Last five actions are:")
        for i in range(len(array)-5,len(array)):
            handle.write(f'Action {i+1}')
            history.append(f'Action {i+1}')
            for key in array[i]:
                handle.write(key+"-"+array[i][key])
                history.append(key + '-' + array[i][key])
    update.message.reply_text("\n".join(history))
    handle.close()       
        


def main():
    bot = Bot(
        token=TOKEN,
        base_url=PROXY,  # delete it if connection via VPN
    )
    updater = Updater(bot=bot, use_context=True)

    # on different commands - answer in Telegram
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', chat_help))

    # on noncommand i.e message - echo the message on Telegram
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()




        
        


if __name__ == '__main__':
    logger.info('Start Bot')
    main()
