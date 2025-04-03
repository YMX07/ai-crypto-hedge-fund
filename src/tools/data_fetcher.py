import ccxt
import yfinance as yf
import pandas as pd
from datetime import datetime
import time

def fetch_crypto_data(tickers, start_date, end_date, timeframe="1d"):
    """
    Fetches historical OHLCV data for specified crypto tickers from KuCoin, Binance, and Yahoo Finance.
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

    # Initialize exchanges
    kucoin = ccxt.kucoin()
    binance = ccxt.binance()

    # Map tickers to exchange symbols (e.g., BTC -> BTC/USDT for ccxt, BTC-USD for yfinance)
    ticker_to_symbol = {
        ticker: {
            "ccxt": f"{ticker}/USDT",  # KuCoin and Binance use USDT pairs
            "yfinance": f"{ticker}-USD"  # Yahoo Finance uses -USD suffix
        } for ticker in tickers
    }

    # Dictionary to store aggregated data for each ticker
    aggregated_data = {ticker: [] for ticker in tickers}

    # Fetch data from KuCoin
    for ticker in tickers:
        symbol = ticker_to_symbol[ticker]["ccxt"]
        try:
            ohlcv = kucoin.fetch_ohlcv(symbol, timeframe, since=start_ts, limit=None)
            df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df["source"] = "kucoin"
            df["ticker"] = ticker
            aggregated_data[ticker].append(df)
        except Exception as e:
            print(f"Error fetching {ticker} from KuCoin: {e}")

    # Fetch data from Binance
    for ticker in tickers:
        symbol = ticker_to_symbol[ticker]["ccxt"]
        try:
            ohlcv = binance.fetch_ohlcv(symbol, timeframe, since=start_ts, limit=None)
            df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df["source"] = "binance"
            df["ticker"] = ticker
            aggregated_data[ticker].append(df)
        except Exception as e:
            print(f"Error fetching {ticker} from Binance: {e}")

    # Fetch data from Yahoo Finance
    for ticker in tickers:
        symbol = ticker_to_symbol[ticker]["yfinance"]
        try:
            yf_data = yf.download(symbol, start=start_date, end=end_date, interval="1d")
            if not yf_data.empty:
                df = yf_data.reset_index()
                df = df.rename(columns={
                    "Date": "timestamp",
                    "Open": "open",
                    "High": "high",
                    "Low": "low",
                    "Close": "close",
                    "Volume": "volume"
                })
                df["source"] = "yahoo"
                df["ticker"] = ticker
                df = df[["timestamp", "open", "high", "low", "close", "volume", "source", "ticker"]]
                aggregated_data[ticker].append(df)
        except Exception as e:
            print(f"Error fetching {ticker} from Yahoo Finance: {e}")

    # Aggregate and normalize data
    result = {}
    for ticker in tickers:
        if not aggregated_data[ticker]:  # Skip if no data was fetched
            print(f"No data fetched for {ticker}")
            continue

        # Concatenate data from all sources
        combined_df = pd.concat(aggregated_data[ticker], ignore_index=True)

        # Ensure timestamp is in datetime format
        combined_df["timestamp"] = pd.to_datetime(combined_df["timestamp"])

        # Filter data within the date range
        combined_df = combined_df[
            (combined_df["timestamp"] >= start_date) & (combined_df["timestamp"] <= end_date)
        ]

        # Group by timestamp and average the OHLCV values across sources
        aggregated_df = combined_df.groupby("timestamp").agg({
            "open": "mean",
            "high": "mean",
            "low": "mean",
            "close": "mean",
            "volume": "mean"
        }).reset_index()

        # Sort by timestamp
        aggregated_df = aggregated_df.sort_values("timestamp")

        # Reset index and ensure all columns are present
        aggregated_df = aggregated_df[["timestamp", "open", "high", "low", "close", "volume"]]

        result[ticker] = aggregated_df

    return result

