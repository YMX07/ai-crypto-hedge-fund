from tabulate import tabulate
from colorama import Fore, Style

def print_trading_output(result):
    """
    Prints the trading decisions and analyst signals in a formatted table.
    Args:
        result (dict): Result containing 'decisions' and 'analyst_signals'
    """
    decisions = result.get("decisions", {})
    analyst_signals = result.get("analyst_signals", {})

    if not decisions:
        print("No trading decisions generated.")
        return

    # Print trading decisions
    print("\n" + Fore.CYAN + Style.BRIGHT + "Final Trading Decisions:" + Style.RESET_ALL)
    decision_table = []
    for ticker, decision in decisions.items():
        decision_table.append([
            ticker,
            decision.get("action", "hold"),
            f"{decision.get('size', 0):.2f}",
            f"{decision.get('confidence', 0):.2f}"
        ])
    print(tabulate(decision_table, headers=["Ticker", "Action", "Size", "Confidence"], tablefmt="fancy_grid"))

    # Print analyst signals
    print("\n" + Fore.CYAN + Style.BRIGHT + "Analyst Signals:" + Style.RESET_ALL)
    for analyst, signals in analyst_signals.items():
        print(f"\n{Fore.GREEN}{analyst.replace('_', ' ').title()}{Style.RESET_ALL}:")
        signal_table = []
        for ticker, signal in signals.items():
            signal_table.append([
                ticker,
                signal.get("action", "hold"),
                f"{signal.get('confidence', 0):.2f}",
                signal.get("reasoning", "")
            ])
        print(tabulate(signal_table, headers=["Ticker", "Action", "Confidence", "Reasoning"], tablefmt="fancy_grid"))