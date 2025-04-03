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
            buy_conf = sum(s["confidence"] for s in asset_sigs if s["action"] == "buy") / len(asset_sigs)
            sell_conf = sum(s["confidence"] for s in asset_sigs if s["action"] == "sell") / len(asset_sigs)

            if buy_conf > 0.8:
                decisions.append(
                    {"action": "buy", "asset": asset, "size": self.max_position_size, "confidence": buy_conf})
            elif sell_conf > 0.8:
                decisions.append(
                    {"action": "sell", "asset": asset, "size": self.max_position_size, "confidence": sell_conf})
            else:
                decisions.append(
                    {"action": "hold", "asset": asset, "size": 0.0, "confidence": max(buy_conf, sell_conf)})

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
            continue

        buy_conf = sum(s["confidence"] for s in ticker_signals if s["action"] == "buy") / len(ticker_signals)
        sell_conf = sum(s["confidence"] for s in ticker_signals if s["action"] == "sell") / len(ticker_signals)

        if buy_conf > 0.8:
            decisions[ticker] = {"action": "buy", "size": 0.2, "confidence": buy_conf}
        elif sell_conf > 0.8:
            decisions[ticker] = {"action": "sell", "size": 0.2, "confidence": sell_conf}
        else:
            decisions[ticker] = {"action": "hold", "size": 0.0, "confidence": max(buy_conf, sell_conf)}

    state["messages"].append(AIMessage(content=str(decisions)))
    return state
