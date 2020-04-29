#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import logging
from setup import PROXY, TOKEN
from telegram import Bot, Update
import datetime
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater
from classes import WorkWithCoronaData, Website, WorkWithCsvTable, WriteDb

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
array = []


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def analise(function):
    def inner(*args, **kwargs):
        update = args[0]
        if update and hasattr(update, 'message') and hasattr(update, 'effective_user'):
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


def write_history(update: Update, array):
    with open("history.txt", "w") as handle:
        history = []
        if len(array) == 0:
            handle.write("There are not actions\n")
        elif len(array) > 0:
            handle.write("Last actions are:\n")
            for i in range(0, len(array)):
                handle.write(f'Action {i + 1}:\n')
                history.append(f'Action {i + 1}:')
                for key in array[i]:
                    handle.write(key + " : " + array[i][key] + "\n")
                    history.append(key + ' : ' + array[i][key])
    return history


def write_facts(update: Updater, url):
    web = Website(url)
    s = Website.get_data(web)
    if s is not None:
        ma = 0
        al = s['all']
        data = ''
        for i in range(len(al)):
            if al[i]['upvotes'] > ma and al[i]['type'] == 'cat':
                ma = al[i]['upvotes']
                data = ''
                data += f'User: {al[i]["user"]["name"]["first"]} {al[i]["user"]["name"]["last"]}\n' \
                    f'{al[i]["text"]}\nLikes: {al[i]["upvotes"]}'
        return data
    else:
        return ''


def write_database(direct, name, ind, data):
    data_new = WorkWithCsvTable(data=[])
    file = direct+name[0]+'-'+name[1]+'-'+name[2]+ind+'.csv'
    data_new.data = data
    data_new.write_table(file)
    db = WriteDb()
    db.file = file
    db.write_db(name[0] + '-' + name[1] + '-' + name[2], ind)


def corona_write(update: Updater):
    answer = ''
    corona0 = WorkWithCoronaData([], [0] * 1000, [], [], {}, 0)
    WorkWithCoronaData.provinces(corona0)
    data = []
    for elem in corona0.count[:5]:
        for row in corona0.prov:
            for key, value in row.items():
                if value[1] == elem:
                    data.append({'Place': value[0], 'Active': value[1]})
                    answer += f"{value[0]}: {value[1]}\n"
    write_database("data\\", corona0.data1, 'prov', data)
    return answer


def corona_dynamics_write(update: Updater):
    answer = ''
    corona0 = WorkWithCoronaData([], [0] * 1000, [], [], {}, 0)
    corona1 = WorkWithCoronaData([], [0] * 1000, [], [], {}, 1)
    WorkWithCoronaData.corona_dynamics(corona0)
    WorkWithCoronaData.corona_dynamics(corona1)
    data_1, data = [], []
    for elem in corona0.count[:5]:
        for key, value in corona0.now.items():
            for key1, value1 in corona1.now.items():
                if key == key1 and value[4] == elem:
                    data.append({"Country_Region": value[0], "Confirmed": value[1],
                                "Deaths": value[2], "Recovered": value[3], "Active": value[4]})
                    data_1.append({"Country_Region": value1[0], "Confirmed": value1[1],
                                   "Deaths": value1[2], "Recovered": value1[3], "Active": value1[4]})
                    answer += f'{str(value[0]).upper()}\n'
                    answer += f'Confirmed: {value[1] - value1[1]} Deaths: {value[2] - value1[2]} Recovered:' \
                        f' {value[3] -value1[3]} Active: {value[4] - value1[4]}\n'
    write_database('data\\', corona0.data1, 'dyn', data)
    write_database('data\\', corona1.data1, 'dyn', data_1)
    return answer


def corona_russia_write(update: Updater):
    answer = ''
    corona0 = WorkWithCoronaData([], [0] * 1000, [], [], {}, 0)
    corona1 = WorkWithCoronaData([], [0] * 1000, [], [], {}, 1)
    WorkWithCoronaData.corona_russia(corona0)
    WorkWithCoronaData.corona_russia(corona1)
    data_1, data = [], []
    for key, value in corona0.now.items():
        for key1, value1 in corona1.now.items():
            data.append({"Country_Region": value[0], "Confirmed": value[1],
                        "Deaths": value[2], "Recovered": value[3], "Active": value[4]})
            data_1.append({"Country_Region": value1[0], "Confirmed": value1[1],
                           "Deaths": value1[2], "Recovered": value1[3], "Active": value1[4]})
            answer += f'{str(value[0]).upper()}\n'
            answer += f'Confirmed: {value[1] - value1[1]} Deaths: {value[2] - value1[2]} Recovered: ' \
                f'{value[3] - value1[3]} Active: {value[4] - value1[4]}\n'
    write_database('data\\', corona0.data1, 'rus', data)
    write_database('data\\', corona1.data1, 'rus', data_1)
    return answer


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
    history_data = write_history(update, array)
    if len(array) > 0:
        update.message.reply_text("Last actions are:\n" + "\n".join(history_data))
    else:
        update.message.reply_text("There are not actions")


@decorator_error
@analise
def facts(update: Updater, context: CallbackContext):
    url = 'https://cat-fact.herokuapp.com/facts'
    text = write_facts(update, url)
    update.message.reply_text(text)


@decorator_error
@analise
def corona(update: Updater, context: CallbackContext):
    answer = 'Пять провинций с наибольшим кол-вом зараженных COVID-19:\n'
    db = WriteDb()
    data1 = datetime.date.today().strftime("%m-%d-%Y")
    day = str(int(data1[3]) * 10 + int(data1[4]) - 1)
    data2 = data1[:3] + day + data1[5:]
    data = db.find_doc(data2, 'prov')
    if data:
        for row in data:
            for key, value in row.items():
                if key != '_id' and (key == "Place"):
                    answer += f"{value}:"
                elif key != '_id':
                    answer += f"{value}\n"
    else:
        answer += corona_write(update)
    update.message.reply_text(answer)


@decorator_error
@analise
def corona_dynamics(update: Updater, context: CallbackContext):
    answer = 'Динамика заражений COVID-19 за два дня для Топ-5 стран:\n'
    db = WriteDb()
    data1 = datetime.date.today().strftime("%m-%d-%Y")
    data = db.find_doc(data1, 'dyn')
    day = str(int(data1[3]) * 10 + int(data1[4]) - 1)
    data2 = data1[:3] + day + data1[5:]
    data_1 = db.find_doc(data2, 'dyn')
    if data and data_1:
        for key, value in data.items():
            for key1, value1 in data_1.items():
                if key == key1 and key != '_id':
                    if key == "Country_Region":
                        answer += f'{str(value).upper()}\n'
                    else:
                        answer += f'{key}: {value - value1} '
        answer += '\n'
    else:
        answer += corona_dynamics_write(update)
    update.message.reply_text(answer)


@decorator_error
@analise
def corona_russia(update: Updater, context: CallbackContext):
    answer = 'Динамика заражений COVID-19 за два дня для России:\n'
    db = WriteDb()
    data1 = datetime.date.today().strftime("%m-%d-%Y")
    data = db.find_doc(data1, 'rus')
    day = str(int(data1[3]) * 10 + int(data1[4]) - 1)
    data2 = data1[:3] + day + data1[5:]
    data_1 = db.find_doc(data2, 'rus')
    if data and data_1:
        for key, value in data.items():
            for key1, value1 in data_1.items():
                if key == key1 and key != '_id':
                    if key == "Country_Region":
                        answer += f'{str(value).upper()}\n'
                    else:
                        answer += f'{key}: {value-value1} '
        answer += '\n'
    else:
        answer += corona_russia_write(update)
    update.message.reply_text(answer)


@decorator_error
@analise
def info(update: Updater, context: CallbackContext):
    answer = 'Команды для работы с ботом:\n/start-Приветствие\n/help-Подсказка с чего начать\n' \
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
