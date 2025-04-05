from tabulate import tabulate

def print_trading_output(result):
    """
    Prints the trading output in the desired format.
    Args:
        result (dict): Dictionary containing decisions and analyst signals.
    """
    decisions = result["decisions"]
    analyst_signals = result["analyst_signals"]

    # Step 1: Analysis for each ticker
    tickers = sorted(decisions.keys())  # Sort tickers alphabetically
    for ticker in tickers:
        print(f"\nANALYSIS FOR {ticker}\n")
        # Collect signals for this ticker from all analysts
        for analyst, signals in analyst_signals.items():
            if ticker in signals:
                signal = signals[ticker]
                print(f"AGENT: {analyst}")
                print(f"SIGNAL: {signal['action'].upper()}")
                print(f"CONFIDENCE: {signal['confidence'] * 100:.1f}%")
                print(f"REASONING: {signal.get('reasoning', 'No reasoning provided.')}\n")

    # Step 2: Final Trading Decisions
    print("\nFinal Trading Decisions:")
    table = []
    for ticker in tickers:
        decision = decisions[ticker]
        table.append([ticker, decision["action"], decision["size"], decision["confidence"]])
    print(tabulate(table, headers=["Ticker", "Action", "Size", "Confidence"], tablefmt="fancy_grid"))

    # Step 3: Analyst Signals (recap table)
    print("\nAnalyst Signals:\n")
    table = []
    for ticker in tickers:
        for analyst, signals in analyst_signals.items():
            if ticker in signals:
                signal = signals[ticker]
                table.append([ticker, analyst, signal["action"], f"{signal['confidence'] * 100:.1f}%", signal.get("reasoning", "No reasoning provided.")])
    # Limit column widths for better readability
    print(tabulate(table, headers=["Ticker", "Analyst", "Action", "Confidence", "Reasoning"], tablefmt="fancy_grid", maxcolwidths=[10, 20, 10, 10, 50]))