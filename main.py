import time
from bybit import bybit
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN, CHAT_ID  # Importing the token and chat ID
from bybit_config import BYBIT_API_KEY, BYBIT_API_SECRET  # Importing ByBit API keys

# Initialize the ByBit client
client = bybit(test=False, api_key=BYBIT_API_KEY, api_secret=BYBIT_API_SECRET)

def fetch_bybit_tickers(min_volume=50000000):
    try:
        # Fetch the tickers
        response = client.Market.Market_symbolInfo().result()
        tickers = response[0]  # The first element contains the data
        
        filtered_tickers = []
        for ticker_info in tickers:
            volume_now = float(ticker_info['volume_24h'])
            if volume_now >= min_volume:
                filtered_tickers.append({
                    "ticker": ticker_info['symbol'],
                    "current_price": ticker_info['last_price'],
                    "volume_now": volume_now,
                })
        return filtered_tickers
    except Exception as e:
        print("Error fetching data from ByBit API:", e)
        return None

def send_to_telegram(bot_token, chat_id, message):
    bot = Bot(token=bot_token)
    bot.send_message(chat_id=chat_id, text=message)

def main():
    tickers = fetch_bybit_tickers(min_volume=50000000)
    if tickers:
        for ticker in tickers:
            message = f"Potentially Pump for {ticker['ticker']}\n" \
                      f"Current Price: {ticker['current_price']}\n" \
                      f"Volume Now: {ticker['volume_now']}\n"
            send_to_telegram(TELEGRAM_BOT_TOKEN, CHAT_ID, message)

if __name__ == "__main__":
    main()
