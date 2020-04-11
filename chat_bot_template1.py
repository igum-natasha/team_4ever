#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import logging
import requests
from setup import PROXY, TOKEN
from telegram import Bot, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater
from classes import WorkWithCoronaData,Website

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
array=[]
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def analise(function):
    def inner(*args, **kwargs):
        update = args[0]
        if update and hasattr(update, 'message') and hasattr(update,'effective_user'):
            array.append({
                "user": update.effective_user.first_name,
                "function": function.__name__,
                "message": update.message.text})
        return function(*args, **kwargs)
    return inner

def decorator_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SyntaxError:
            update = args[0]
            if update:
                update.message.reply_text(f'Error! Function:{func.__name__}')
    return inner



        
@decorator_error
@analise
def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'Привет, {update.effective_user.first_name}!')

@decorator_error
@analise
def chat_help(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Введи команду /start для начала. ')



@analise
def echo(update: Update, context: CallbackContext):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

@analise
def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning(f'Update {update} caused error {context.error}')

@decorator_error
@analise
def history(update: Updater, context: CallbackContext):
    with open("history.txt", "w") as handle:
        history =[]
        if len(array) == 0:
            handle.write("There are not actions\n")
            update.message.reply_text("There are not actions")
        elif len(array) >0:
            handle.write("Last actions are:\n")
            update.message.reply_text("Last actions are:")
            for i in range(0, len(array)):
                handle.write(f'Action {i+1}:\n')
                history.append(f'Action {i+1}:')
                for key in array[i]:
                    handle.write(key+" : "+array[i][key]+"\n")
                    history.append(key + ' : ' + array[i][key])
        update.message.reply_text("\n".join(history))

@decorator_error
@analise
def facts(update: Updater, context: CallbackContext):
    s=Website.get_data('https://cat-fact.herokuapp.com/facts')
    ma = 0
    all=s['all']
    for i in range(len(all)):
        if all[i]['upvotes'] > ma and all[i]['type']=='cat':
            ma = all[i]['upvotes']
            update.message.reply_text(f'User: {all[i]["user"]["name"]["first"]} {all[i]["user"]["name"]["last"]}\n{all[i]["text"]}\nLikes: {all[i]["upvotes"]}')

@decorator_error
@analise
def corona(update: Updater, context: CallbackContext):
    answer = 'Пять провинций с наибольшим кол-вом зараженных COVID-19:\n'
    corona=WorkWithCoronaData
    corona.prov={}
    corona.count=[]
    corona.provinces()
    for elem in corona.count[:5]:
        for key, value in corona.prov.items():
            if value == elem:
                answer += f"{key} : {value}\n"
    update.message.reply_text(answer)

@decorator_error
@analise
def corona_dynamics(update: Updater, context: CallbackContext):
    answer='Динамика заражений COVID-19 за два дня для Топ-5 стран:\n'
    corona = WorkWithCoronaData
    corona1=WorkWithCoronaData
    corona.count,corona1.count1=[0]*1000,[0]*1000
    now=WorkWithCoronaData.corona_dynamics(0)
    now1=WorkWithCoronaData.corona_dynamics(1)
    for elem in corona.count[:5]:
        for key,value in corona.now.items():
            for key1,value1 in corona1.now1.items():
                if key==key1 and value[4]==elem:
                    answer+=f'{str(value[0]).upper()}\n'
                    answer+=f'Confirmed: {value[1]-value1[1]} Deaths: {value[2]-value1[2]} Recovered: {value[3]-value1[3]} Active: {value[4]-value1[4]}\n'
    update.message.reply_text(answer)

@decorator_error
@analise
def corona_russia(update: Updater, context: CallbackContext):
    answer='Динамика заражений COVID-19 за два дня для России:\n'
    corona = WorkWithCoronaData
    corona1 = WorkWithCoronaData
    corona.count, corona1.count1 = [0] * 1000, [0] * 1000
    now = WorkWithCoronaData.corona_dynamics(0)
    now1 = WorkWithCoronaData.corona_dynamics(1)
    for key,value in corona.now.items():
            for key1,value1 in corona1.now1.items():
                    answer+=f'{str(value[0]).upper()}\n'
                    answer+=f'Confirmed: {value[1]-value1[1]} Deaths: {value[2]-value1[2]} Recovered: {value[3]-value1[3]} Active: {value[4]-value1[4]}\n'
    update.message.reply_text(answer)

@decorator_error
@analise
def info(update: Updater, context: CallbackContext):
    answer='Команды для работы с ботом:\n/start-Приветствие\n/help-Подсказка с чего начать\n' \
           '/history-История последних запросов\n/facts-Самый популярный факт о котах\n' \
           '/corona_stats-Пять провинций с наибольшим кол-вом зараженных\n ' \
           '/corona_dynamics-Динамика заражений COVID-19 за два дня для Топ-5 стран\n' \
           '/corona_russia-Динамика заражения COVID-19 за два дня для России\n'
    update.message.reply_text(answer)

def main():
    bot = Bot(
        token=TOKEN,
        base_url=PROXY,  # delete it if connection via VPN
    )
    updater = Updater(bot=bot, use_context=True)

    # on different commands - answer in Telegram
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', chat_help))
    updater.dispatcher.add_handler(CommandHandler('history', history))
    updater.dispatcher.add_handler(CommandHandler('facts', facts))
    updater.dispatcher.add_handler(CommandHandler('corona_stats', corona))
    updater.dispatcher.add_handler(CommandHandler('corona_dynamics', corona_dynamics))
    updater.dispatcher.add_handler(CommandHandler('corona_russia', corona_russia))
    updater.dispatcher.add_handler(CommandHandler('info', info))
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
