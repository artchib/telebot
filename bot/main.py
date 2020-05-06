# coding: utf8
# -*- coding: utf-8 -*-
from telegram import Bot
from telegram import Update
from telegram.ext import Updater, CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram.ext import Filters
from bot.bittrex import BittrexClient
from bot.bittrex import BittrexError
from logging import getLogger
from bot.config import load_config

config = load_config()
logger = getLogger(__name__)

USD_BTC_PAIR = 'USD-BTC'
USD_DASH_PAIR = 'USD-DASH'
BTC_TO_USD_BUTT = 'BTC--->USD'
USD_TO_BTC_BUTT = 'USD--->BTC'

# def get_convert_keyboard():
#     keyboard = [
#         [
#             KeyboardButton(BTC_TO_USD_BUTT),
#             KeyboardButton(USD_TO_BTC_BUTT),
#
#         ],
#     ]
#     return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def back_button():

    keyboard = [
            [InlineKeyboardButton('Назад', callback_data=f'btmk')],
        ]
    return InlineKeyboardMarkup(keyboard)


def get_main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text=BTC_TO_USD_BUTT, callback_data='btc_to_usd')
         ],
        [
            InlineKeyboardButton(text=USD_TO_BTC_BUTT, callback_data='usd_to_btc')
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def button_callback_handler(update: Update, context: CallbackContext,):
    query = update.callback_query
    call_data = query.data
    print(call_data)
    global cur_to_cur

    if call_data == 'btc_to_usd':
        client = BittrexClient()
        global rate_btc
        rate_btc = client.get_last_price(pair=USD_BTC_PAIR)
        text = f'Сейчас за один биткоин дают {rate_btc} долларов\n Введите кол-во BTC:'
        print(f'srabotal btc--usd ----- {rate_btc}')
        cur_to_cur = 'BTC_USD'
        query.edit_message_text(
            text=text,
            reply_markup=back_button()
        )

    if call_data == 'usd_to_btc':
        client = BittrexClient()
        rate_btc = client.get_last_price(pair=USD_BTC_PAIR)
        text = f'Сейчас за один доллар дают {1/rate_btc} биткойнов\n Введите кол-во $:'
        print(f'srabotal btc--usd ----- {rate_btc}')
        cur_to_cur = 'USD_BTC'
        query.edit_message_text(
            text=text,
            reply_markup=back_button()
        )


    if call_data == 'converter':
        # print('RABOTAET KONVERTER')
        # query.edit_message_text(
        #     text='Это ковертер',
        #     reply_markup=get_convert_keyboard(),
        # )

        pass


    if call_data == 'btmk':
        print('srabotal BACK')
        query.edit_message_text(
            text='Что на Что меняем?',
            reply_markup=get_main_keyboard(),
        )


def do_start(update: Update, context: CallbackContext):
    global cur_to_cur
    cur_to_cur = ''
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Что на Что меняем АААААААА?',
        reply_markup= get_main_keyboard(),
    )

def do_text(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = update.message.text
    global cur_to_cur, rate_btc
    if message.isdigit():
        print(f'сообщение цифра, cur_to_cur={cur_to_cur}, цифра = {message}')
        if cur_to_cur != '':
            if cur_to_cur == 'BTC_USD':
                text = f'= {float(message) * rate_btc} $'
            elif cur_to_cur == 'USD_BTC':
                text = f'= {float(message) / rate_btc} BTC'
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text='Не выбрано направление обмена',
                reply_markup=get_main_keyboard(),
            )
        context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=get_main_keyboard(),
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text='Вы ввели текст, а не цифрууууу',
         #   reply_markup=get_main_keyboard(),
        )



def main():
    logger.info("Запускаем бота...")
    bot = Bot(
        token=config.TG_TOKEN,
    )
    updater = Updater(
        bot=bot,
        use_context=True,
    )

    info = bot.getMe()
    logger.info(f'Bot info: {info}')

    global cur_to_cur

    start_handler = CommandHandler('start', do_start)
    buttons_handler = CallbackQueryHandler(callback=button_callback_handler)
    text_handler = MessageHandler(Filters.text, do_text)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(buttons_handler)
    updater.dispatcher.add_handler(text_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
