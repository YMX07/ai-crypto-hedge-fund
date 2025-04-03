import matplotlib.pyplot as plt
import pandas as pd

def plot_portfolio_value(backtest_results):
    """
    Plots the portfolio value over time.
    Args:
        backtest_results (pd.DataFrame): DataFrame with 'timestamp' and 'portfolio_value' columns
    """
    plt.figure(figsize=(12, 6))
    plt.plot(backtest_results['timestamp'], backtest_results['portfolio_value'], label='Portfolio Value', color='blue')
    plt.title('Portfolio Value Over Time')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value (USD)')
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_drawdowns(backtest_results):
    """
    Plots the drawdowns over time.
    Args:
        backtest_results (pd.DataFrame): DataFrame with 'timestamp' and 'drawdown' columns
    """
    plt.figure(figsize=(12, 6))
    plt.plot(backtest_results['timestamp'], backtest_results['drawdown'], label='Drawdown', color='red')
    plt.title('Drawdowns Over Time')
    plt.xlabel('Date')
    plt.ylabel('Drawdown (%)')
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_returns(backtest_results):
    """
    Plots the cumulative returns over time.
    Args:
        backtest_results (pd.DataFrame): DataFrame with 'timestamp' and 'cumulative_returns' columns
    """
    plt.figure(figsize=(12, 6))
    plt.plot(backtest_results['timestamp'], backtest_results['cumulative_returns'], label='Cumulative Returns', color='green')
    plt.title('Cumulative Returns Over Time')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns (%)')
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()