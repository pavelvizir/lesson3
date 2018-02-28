#!/usr/bin/env python
'''
Задание

    1. Установите модуль ephem
    2. Добавьте в бота команду /planet, которая будет принимать на вход
        название планеты на английском.
    3. При помощи условного оператора if и ephem.constellation научите бота
        отвечать, в каком созвездии сегодня находится планета.

'''

import logging
from datetime import datetime

import ephem
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton

from bot_token import bot_token

LIST_OF_PLANETS = list(
    a[2] for a in ephem._libastro.builtin_planets() if a[1] == 'Planet')

logging.basicConfig(
    format='%(asctime)s: %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log')


def greet_user(bot, update):

    text = 'Вызван /start'
    print(text)
    print(update)
    update.message.reply_text(text)

def calc_check_args(args_str):
    calc_result = None
    if not args_str.endswith('='):    
        calc_result = "Operation should look like 1+2="
    elif not (args_str[0].isdigit() and args_str[2].isdigit()):
        calc_result = "There should be two 1 digit numbers"
    elif args_str[1] == '/' and not int(args_str[2]): 
        calc_result = "Do not divide by zero."
    #print(calc_result)
    return calc_result    


def calc(bot,update,args):
    args_str = list(args)[0]
    text = 'Вызван /calc ' + args_str
    print(text)
    #operation = {'+': sum; '-': sub, '/': mod,  }
    calc_result = calc_check_args(args_str)
    if not calc_result:
        print(calc_result)
        print(args_str)
        first = int(args_str[0])
        second = int(args_str[2])
        if args_str[1] == '+':
            calc_result = first + second
        elif args_str[1] == '-':
            calc_result = first - second
        elif args_str[1] == '*':
            calc_result = first + second
        elif args_str[1] == '/':
            calc_result = first / second
        else:
            calc_result = "Operation shoud be *+-/"

    print(calc_result)
    update.message.reply_text(calc_result)

def calc_with_keyboard(bot,update):
    #chat_id = bot.get_updates()[-1].message.chat_id
    chat_id = update.message.chat_id
    reply_markup = ReplyKeyboardRemove()
    bot.send_message(chat_id=chat_id, text="I'm back.", reply_markup=reply_markup)
    
    #custom_keyboard = [['1', '2', '3', '+'], 
    #                    ['4', '5', '6', '-'],
    #                    ['7', '8', '9', '/'],
    #                    ['0', '*']]
    #reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    #bot.send_message(chat_id=chat_id, 
    #                  text="Custom Keyboard Test", 
    #                  reply_markup=reply_markup)

    button_list = [
    InlineKeyboardButton("col1", callback_data=...),
    InlineKeyboardButton("col2", callback_data=...),
    InlineKeyboardButton("row 2", callback_data=...)
    ]
    reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=2))
    bot.send_message(chat_id = chat_id, text = "A two-column menu", reply_markup=reply_markup)

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

    

def wordcount(bot,update, args):
    text = 'Вызван /wordcount'
    print(text)
    print(list(args))
    args_list = list(args)
    if not args_list:
    #    reply_ffs = args_list[1].count(' ')
        reply_ffs = 0

    elif not (' '.join(args_list).startswith('"') and ' '.join(args_list).endswith('"')):
        reply_ffs = 'You should have "" !' 
    else:
        reply_ffs = len(args_list)
    
    update.message.reply_text(reply_ffs)


def get_constellation(bot, planet, args):


    text = 'Вызван /planet'
    planet_name = ''.join(args)
    print(text)
    print(planet)
    #planet.message.reply_text(list(args))
    if planet_name in LIST_OF_PLANETS:
        planet_object = getattr(ephem, planet_name)
        constellation = ephem.constellation(
                planet_object(datetime.now().strftime('%Y/%m/%d')))
        print(constellation)
        planet.message.reply_text(constellation)
    else:
        constellaton = "No such planet!"
        print(constellaton)
        planet.message.reply_text(constellation)


def talk_to_me(bot, update):
    user_text = update.message.text
    print(user_text)
    # update.message.reply_text(user_text[::-1].swapcase())
    update.message.reply_text(user_text[::-1])


def main():
    updater = Updater(bot_token)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("wordcount", wordcount, pass_args=True))
    dp.add_handler(CommandHandler("calc", calc, pass_args=True))
    dp.add_handler(CommandHandler("kalk", calc_with_keyboard))
    dp.add_handler(CommandHandler("planet", get_constellation, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    updater.start_polling()
    updater.idle()


main()
'''
import ephem
from pprint import pprint
from datetime import datetime
pprint(ephem._libastro.builtin_planets())

for i in list(a[2] for a in ephem._libastro.builtin_planets() if a[1] == 'Planet'):
    t = getattr(ephem, i)
    print(ephem.constellation(t(datetime.now().strftime('%Y/%m/%d'))))
    '''
