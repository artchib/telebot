from bot.bittrex import BittrexClient
from bot.bittrex import BittrexError

NOTIFY_PAIR = 'USD-BTC'

def main():
    client = BittrexClient()
    current_price = client.get_last_price(pair=NOTIFY_PAIR)
    print(f'{NOTIFY_PAIR} = {current_price}')

if __name__ == '__main__':
    main()