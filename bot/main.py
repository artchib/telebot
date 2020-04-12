from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton
from bot.bittrex import BittrexClient
from bot.bittrex import BittrexError

from bot.config import TG_TOKEN

USD_BTC_PAIR = 'USD-BTC'
USD_DASH_PAIR = 'USD-DASH'

def back_button():

    keyboard = [
            [InlineKeyboardButton('Назад', callback_data=f'btmk')],
        ]
    return InlineKeyboardMarkup(keyboard)


def get_main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text='Курсы криптовалют', callback_data='rates')
         ],
        [
            InlineKeyboardButton(text='Конвертер', callback_data='converter')
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def button_callback_handler(bot: Bot, update: Update):
    query = update.callback_query
    call_data = query.data
    print(call_data)

    if call_data == 'rates':
        client = BittrexClient()
        rate_btc = client.get_last_price(pair=USD_BTC_PAIR)
        rate_dash = client.get_last_price(pair=USD_DASH_PAIR)
        text = f'Сейчас за один биткоин дают {rate_btc} долларов\n А за один DASH {rate_dash}'
        print(f'srabotal btc--usd ----- {rate_btc}')
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


def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Что на Что меняем?',
        reply_markup= get_main_keyboard(),
    )

def do_text(bot: Bot, update: Update):
    pass


def main():
    bot = Bot(
        token=TG_TOKEN
    )
    updater = Updater(
        bot=bot
    )

    start_handler = CommandHandler('start', do_start)
    buttons_handler = CallbackQueryHandler(callback=button_callback_handler)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(buttons_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
