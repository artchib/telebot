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
BTC_DASH_PAIR = 'BTC-DASH'

BTC_TO_USD_BUTT = 'BTC--->USD'
USD_TO_BTC_BUTT = 'USD--->BTC'
DASH_TO_USD_BUTT = 'DASH--->USD'
USD_TO_DASH_BUTT = 'USD--->DASH'
BTC_TO_DASH_BUTT = 'BTC--->DASH'
DASH_TO_BTC_BUTT = 'DASH--->BTC'

def back_button():

    keyboard = [
            [InlineKeyboardButton('Назад', callback_data=f'btmk')],
        ]
    return InlineKeyboardMarkup(keyboard)


def get_main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text=BTC_TO_USD_BUTT, callback_data='btc_to_usd'),
            InlineKeyboardButton(text=USD_TO_BTC_BUTT, callback_data='usd_to_btc'),
         ],
        [
            InlineKeyboardButton(text=DASH_TO_USD_BUTT, callback_data='dash_to_usd'),
            InlineKeyboardButton(text=USD_TO_DASH_BUTT, callback_data='usd_to_dash'),
        ],
        [
            InlineKeyboardButton(text=BTC_TO_DASH_BUTT, callback_data='btc_to_dash'),
            InlineKeyboardButton(text=DASH_TO_BTC_BUTT, callback_data='dash_to_btc'),
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
        rate = client.get_last_price(pair=USD_BTC_PAIR)
        text = f'Сейчас за один биткоин дают {rate} долларов\n Введите кол-во BTC:'
        print(f'srabotal btc--usd ----- {rate}')
        cur_to_cur = 'BTC_USD'
        query.edit_message_text(
            text=text,
            reply_markup=back_button()
        )

    if call_data == 'usd_to_btc':
        client = BittrexClient()
        rate = client.get_last_price(pair=USD_BTC_PAIR)
        text = f'Сейчас за один доллар дают {1/rate} биткойнов\n Введите кол-во $:'
        print(f'srabotal btc--usd ----- {rate}')
        cur_to_cur = 'USD_BTC'
        query.edit_message_text(
            text=text,
            reply_markup=back_button()
        )

    if call_data == 'dash_to_usd':
        client = BittrexClient()
        rate = client.get_last_price(pair=USD_DASH_PAIR)
        text = f'Сейчас за один DASH дают {rate} долларов\n Введите кол-во DASH:'
        cur_to_cur = 'DASH_USD'
        query.edit_message_text(
            text=text,
            reply_markup=back_button()
        )

    if call_data == 'usd_to_dash':
        client = BittrexClient()
        rate = client.get_last_price(pair=USD_DASH_PAIR)
        text = f'Сейчас за один доллар дают {1/rate} DASH\n Введите кол-во $:'
        cur_to_cur = 'USD_DASH'
        query.edit_message_text(
            text=text,
            reply_markup=back_button()
        )

    if call_data == 'btc_to_dash':
        client = BittrexClient()
        rate = client.get_last_price(pair=BTC_DASH_PAIR)
        text = f'Сейчас за один биткоин дают {1/rate} DASH\n Введите кол-во BTC:'
        cur_to_cur = 'BTC_DASH'
        query.edit_message_text(
            text=text,
            reply_markup=back_button()
        )

    if call_data == 'dash_to_btc':
        client = BittrexClient()
        rate = client.get_last_price(pair=BTC_DASH_PAIR)
        text = f'Сейчас за один DASH дают {rate} биткойнов\n Введите кол-во DASH:'
        cur_to_cur = 'DASH_BTC'
        query.edit_message_text(
            text=text,
            reply_markup=back_button()
        )


    if call_data == 'btmk':
        print('srabotal BACK')
        query.edit_message_text(
            text='Что на Что меняем?',
            reply_markup=get_main_keyboard(),
        )


def do_start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Что на Что меняем ?',
        reply_markup= get_main_keyboard(),
    )

def do_text(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = update.message.text

    def is_digit(string):
        if string.isdigit():
            return True
        else:
            try:
                float(string)
                return True
            except ValueError:
                return False
    print(cur_to_cur)
    if is_digit(message):
        print(f'сообщение цифра, cur_to_cur={cur_to_cur}, цифра = {message}')
        if cur_to_cur != '':
            if cur_to_cur == 'BTC_USD':
                text = f'= {float(message) * rate_btc} $'
            elif cur_to_cur == 'USD_BTC':
                text = f'= {float(message) / rate_btc} BTC'
        else:
            context.bot.send_message(
                chat_id=chat_id,
                text='Не выбрано направление обменаааа',
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
    cur_to_cur = ''
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
