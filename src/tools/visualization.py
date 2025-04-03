import mplfinance as mpf
import pandas as pd


def plot_ohlcv(df, ticker="Asset"):
    """
    Plots OHLCV data as a candlestick chart with volume.
    Args:
        df (pd.DataFrame): DataFrame with 'timestamp', 'open', 'high', 'low', 'close', 'volume' columns
        ticker (str): Name of the asset (for the title)
    """
    # Ensure the DataFrame is indexed by timestamp
    df = df.set_index('timestamp')

    # Define the plot style
    mpf_style = mpf.make_mpf_style(base_mpf_style='yahoo', rc={'font.size': 10})

    # Plot candlestick chart with volume
    mpf.plot(
        df,
        type='candle',
        style=mpf_style,
        title=f'{ticker} Candlestick Chart',
        ylabel='Price (USD)',
        volume=True,
        ylabel_lower='Volume',
        show_nontrading=False
    )