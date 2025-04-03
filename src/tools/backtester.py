import pandas as pd
import numpy as np

class Backtester:
    def __init__(self, initial_cash=100000, transaction_cost=0.001):
        """
        Initializes the backtester.
        Args:
            initial_cash (float): Initial cash in the portfolio (default: $100,000)
            transaction_cost (float): Transaction cost per trade (default: 0.1%)
        """
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.transaction_cost = transaction_cost
        self.holdings = {}  # {ticker: quantity}
        self.trades = []  # List of trades for logging
        self.portfolio_values = []  # Track portfolio value over time

    def run(self, signals, price_data):
        """
        Runs the backtest based on trading signals and price data.
        Args:
            signals (list): List of signal dicts with 'action', 'asset', 'size', 'confidence', 'timestamp'
            price_data (dict): Dictionary of DataFrames with OHLCV data for each ticker
        Returns:
            pd.DataFrame: Backtest results with portfolio value, drawdowns, returns
        """
        # Sort signals by timestamp
        signals = sorted(signals, key=lambda x: x['timestamp'])

        # Initialize results DataFrame
        timestamps = price_data[list(price_data.keys())[0]]['timestamp']
        results = pd.DataFrame(index=timestamps)
        results['portfolio_value'] = self.initial_cash
        results['cash'] = self.initial_cash
        results['holdings_value'] = 0.0

        # Process each signal
        for signal in signals:
            timestamp = signal['timestamp']
            asset = signal['asset']
            action = signal['action']
            size = signal['size']  # Fraction of portfolio to allocate

            # Find the price at the timestamp
            price_df = price_data.get(asset)
            if price_df is None:
                continue
            price_row = price_df[price_df['timestamp'] == timestamp]
            if price_row.empty:
                continue
            price = price_row['close'].iloc[0]

            # Execute trade
            if action == 'buy':
                # Calculate amount to spend
                amount_to_spend = self.cash * size
                cost = amount_to_spend * (1 + self.transaction_cost)
                if cost <= self.cash:
                    quantity = amount_to_spend / price
                    self.cash -= cost
                    self.holdings[asset] = self.holdings.get(asset, 0) + quantity
                    self.trades.append({
                        'timestamp': timestamp,
                        'action': 'buy',
                        'asset': asset,
                        'quantity': quantity,
                        'price': price,
                        'cost': cost
                    })
            elif action == 'sell':
                # Calculate amount to sell
                quantity_held = self.holdings.get(asset, 0)
                quantity_to_sell = quantity_held * size
                if quantity_to_sell > 0:
                    revenue = quantity_to_sell * price * (1 - self.transaction_cost)
                    self.cash += revenue
                    self.holdings[asset] -= quantity_to_sell
                    if self.holdings[asset] <= 0:
                        del self.holdings[asset]
                    self.trades.append({
                        'timestamp': timestamp,
                        'action': 'sell',
                        'asset': asset,
                        'quantity': quantity_to_sell,
                        'price': price,
                        'revenue': revenue
                    })

            # Update portfolio value at this timestamp
            holdings_value = 0
            for asset, quantity in self.holdings.items():
                asset_price = price_data[asset][price_data[asset]['timestamp'] == timestamp]['close']
                if not asset_price.empty:
                    holdings_value += quantity * asset_price.iloc[0]
            total_value = self.cash + holdings_value
            results.loc[timestamp, 'portfolio_value'] = total_value
            results.loc[timestamp, 'cash'] = self.cash
            results.loc[timestamp, 'holdings_value'] = holdings_value

        # Forward-fill portfolio values for missing timestamps
        results = results.ffill()

        # Calculate performance metrics
        results['returns'] = results['portfolio_value'].pct_change().fillna(0)
        results['cumulative_returns'] = (1 + results['returns']).cumprod() * 100 - 100  # In percentage
        results['rolling_max'] = results['portfolio_value'].cummax()
        results['drawdown'] = (results['portfolio_value'] - results['rolling_max']) / results['rolling_max'] * 100  # In percentage

        # Reset index to make timestamp a column
        results = results.reset_index()

        return results

    def calculate_metrics(self, results):
        """
        Calculates performance metrics from backtest results.
        Args:
            results (pd.DataFrame): Backtest results DataFrame
        Returns:
            dict: Performance metrics (e.g., Sharpe ratio, max drawdown)
        """
        total_return = (results['portfolio_value'].iloc[-1] / self.initial_cash - 1) * 100
        annualized_return = ((1 + total_return / 100) ** (252 / len(results)) - 1) * 100
        sharpe_ratio = results['returns'].mean() / results['returns'].std() * (252 ** 0.5) if results['returns'].std() != 0 else 0
        max_drawdown = results['drawdown'].min()

        return {
            'total_return': total_return,
            'annualized_return': annualized_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown
        }