import pandas as pd
from datetime import datetime
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def normalize_ohlcv_data(df):
    """
    Normalizes OHLCV data into a standard format.
    Args:
        df (pd.DataFrame): DataFrame with potential variations in column names
    Returns:
        pd.DataFrame: Normalized DataFrame with columns: timestamp, open, high, low, close, volume
    """
    # Standardize column names
    column_mapping = {
        'Date': 'timestamp',
        'Time': 'timestamp',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume',
        'date': 'timestamp',
        'open': 'open',
        'high': 'high',
        'low': 'low',
        'close': 'close',
        'volume': 'volume'
    }

    df = df.rename(columns=column_mapping)

    # Ensure required columns are present
    required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    for col in required_columns:
        if col not in df.columns:
            logger.warning(f"Missing column {col}, filling with NaN")
            df[col] = pd.NA

    # Convert timestamp to datetime if it isn't already
    if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
        try:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        except Exception as e:
            logger.error(f"Failed to convert timestamp: {e}")
            raise ValueError("Could not convert timestamp column to datetime")

    # Convert numeric columns to float
    numeric_cols = ['open', 'high', 'low', 'close', 'volume']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows with missing critical data
    df = df.dropna(subset=['timestamp', 'close'])

    # Sort by timestamp
    df = df.sort_values('timestamp').reset_index(drop=True)

    return df[required_columns]


def date_to_timestamp(date_str, format="%Y-%m-%d"):
    """
    Converts a date string to a Unix timestamp in milliseconds.
    Args:
        date_str (str): Date string (e.g., "2024-01-01")
        format (str): Date format (default: "%Y-%m-%d")
    Returns:
        int: Unix timestamp in milliseconds
    """
    try:
        dt = datetime.strptime(date_str, format)
        return int(dt.timestamp() * 1000)
    except Exception as e:
        logger.error(f"Failed to convert date {date_str} to timestamp: {e}")
        raise ValueError(f"Invalid date format: {date_str}")


def calculate_returns(df):
    """
    Calculates daily returns from the close prices.
    Args:
        df (pd.DataFrame): DataFrame with 'close' column
    Returns:
        pd.Series: Daily returns
    """
    if 'close' not in df.columns:
        logger.error("DataFrame missing 'close' column for return calculation")
        raise ValueError("DataFrame must contain 'close' column")

    returns = df['close'].pct_change().fillna(0)
    return returns


def calculate_volatility(df, window=30):
    """
    Calculates rolling volatility (standard deviation of returns).
    Args:
        df (pd.DataFrame): DataFrame with 'close' column
        window (int): Rolling window size (default: 30)
    Returns:
        pd.Series: Rolling volatility
    """
    returns = calculate_returns(df)
    volatility = returns.rolling(window=window).std() * (252 ** 0.5)  # Annualized volatility
    return volatility


def log_signal(signal):
    """
    Logs a trading signal.
    Args:
        signal (dict): Signal dictionary with action, asset, confidence, reasoning
    """
    logger.info(f"Signal Generated: Action={signal['action']}, Asset={signal['asset']}, "
                f"Confidence={signal['confidence']:.2f}, Reasoning={signal['reasoning']}")


