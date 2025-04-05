import json
from langchain_core.messages import AIMessage


class PortfolioManager:
    def __init__(self):
        self.name = "Portfolio Manager"
        self.max_position_size = 0.2

    def process_signals(self, signals):
        """
        Aggregates agent signals and generates final trading decisions.
        Args:
            signals (list): List of signal dicts from agents
        Returns:
            list: Final trading decisions
        """
        decisions = []
        asset_signals = {}

        for signal in signals:
            asset = signal["asset"]
            if asset not in asset_signals:
                asset_signals[asset] = []
            asset_signals[asset].append(signal)

        for asset, asset_sigs in asset_signals.items():
            # Calculate average confidence for "buy" and "sell" signals
            buy_signals = [s for s in asset_sigs if s["action"] == "buy"]
            sell_signals = [s for s in asset_sigs if s["action"] == "sell"]

            buy_conf = sum(s["confidence"] for s in buy_signals) / len(buy_signals) if buy_signals else 0
            sell_conf = sum(s["confidence"] for s in sell_signals) / len(sell_signals) if sell_signals else 0

            print(f"Confiance pour {asset} - Buy: {buy_conf}, Sell: {sell_conf}")  # Débogage

            if buy_conf > 0.6:  # Threshold for buy decision
                decisions.append(
                    {"action": "buy", "asset": asset, "size": self.max_position_size, "confidence": buy_conf})
            elif sell_conf > 0.6:  # Threshold for sell decision
                decisions.append(
                    {"action": "sell", "asset": asset, "size": self.max_position_size, "confidence": sell_conf})
            else:
                # If no strong buy or sell signal, use the highest confidence among all signals
                max_conf = max(s["confidence"] for s in asset_sigs) if asset_sigs else 0
                action = next(s["action"] for s in asset_sigs if s["confidence"] == max_conf)
                decisions.append(
                    {"action": action, "asset": asset, "size": 0.0 if action == "hold" else self.max_position_size,
                     "confidence": max_conf})

        print(f"Décisions finales (PortfolioManager) : {decisions}")  # Débogage
        return decisions


def portfolio_management_agent(state):
    """
    Aggregates signals and generates final trading decisions.
    Args:
        state (AgentState): The current state with analyst signals
    Returns:
        AgentState: Updated state with final decisions
    """
    analyst_signals = state["data"]["analyst_signals"]
    tickers = state["data"]["tickers"]
    decisions = {}

    for ticker in tickers:
        ticker_signals = []
        for analyst, signals in analyst_signals.items():
            if ticker in signals:
                ticker_signals.append(signals[ticker])

        if not ticker_signals:
            print(f"⚠️ Aucun signal pour {ticker}.")  # Débogage
            continue

        # Calculate average confidence for "buy" and "sell" signals
        buy_signals = [s for s in ticker_signals if s["action"] == "buy"]
        sell_signals = [s for s in ticker_signals if s["action"] == "sell"]

        buy_conf = sum(s["confidence"] for s in buy_signals) / len(buy_signals) if buy_signals else 0
        sell_conf = sum(s["confidence"] for s in sell_signals) / len(sell_signals) if sell_signals else 0

        print(f"Confiance pour {ticker} - Buy: {buy_conf}, Sell: {sell_conf}")  # Débogage

        if buy_conf > 0.6:  # Threshold for buy decision
            decisions[ticker] = {"action": "buy", "size": 0.2, "confidence": buy_conf}
        elif sell_conf > 0.6:  # Threshold for sell decision
            decisions[ticker] = {"action": "sell", "size": 0.2, "confidence": sell_conf}
        else:
            # If no strong buy or sell signal, use the highest confidence among all signals
            max_conf = max(s["confidence"] for s in ticker_signals) if ticker_signals else 0
            action = next(s["action"] for s in ticker_signals if s["confidence"] == max_conf)
            decisions[ticker] = {"action": action, "size": 0.0 if action == "hold" else 0.2, "confidence": max_conf}

    print(f"Décisions finales (portfolio_management_agent) : {decisions}")  # Débogage
    # Use json.dumps to ensure proper JSON formatting with double quotes
    state["messages"].append(AIMessage(content=json.dumps(decisions)))
    return state