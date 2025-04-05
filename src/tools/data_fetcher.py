import ccxt
import pandas as pd
from datetime import datetime

def fetch_crypto_data(tickers, start_date, end_date, timeframe="1d"):
    """
    Fetches historical OHLCV data for specified crypto tickers from Binance.
    Args:
        tickers (list): List of crypto tickers (e.g., ["BTC", "ETH", "ADA"])
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
        timeframe (str): Data timeframe (e.g., "1d" for daily, "1h" for hourly)
    Returns:
        dict: Dictionary mapping tickers to pandas DataFrames with OHLCV data
    """
    # Convert dates to timestamps (required for ccxt)
    start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000)
    end_ts = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp() * 1000)

    # Initialize Binance exchange
    binance = ccxt.binance()

    # Map tickers to Binance symbols
    ticker_to_symbol = {ticker: f"{ticker}/USDT" for ticker in tickers}

    # Dictionary to store aggregated data for each ticker
    result = {}

    for ticker in tickers:
        symbol = ticker_to_symbol[ticker]
        try:
            ohlcv = binance.fetch_ohlcv(symbol, timeframe, since=start_ts, limit=None)

            if not ohlcv:
                print(f"⚠️ Warning: No data fetched for {ticker} from Binance.")
                continue

            df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

            # Sort by timestamp
            df = df.sort_values("timestamp").reset_index(drop=True)
            result[ticker] = df

        except Exception as e:
            print(f"❌ Error fetching {ticker} from Binance: {e}")

    return result