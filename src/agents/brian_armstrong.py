from agents.base_agent import BaseAgent

class BrianArmstrongAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Brian Armstrong")
        self.focus_asset = "BTC"  # Default to BTC as a "blue-chip" crypto

    def generate_signal(self, state):
        """
        Generates a trading signal for the given state.
        Args:
            state (dict): The state containing data, tickers, and signals.
        Returns:
            dict: Updated state with the generated signal.
        """
        # Extraire les données du state
        data = state["data"]
        price_data = data.get("price_data", {})
        tickers = data["tickers"]
        signals = data.get("analyst_signals", {})
        model_name = state["metadata"].get("model_name", "gemini-2.0-flash")
        model_provider = state["metadata"].get("model_provider", "Gemini")

        signals_generated = False
        for ticker in tickers:
            if ticker != self.focus_asset:  # Brian focuses on BTC
                continue

            if ticker not in price_data or price_data[ticker].empty:
                continue

            df = price_data[ticker]
            if "close" not in df.columns:
                continue

            # Générer le signal en utilisant la méthode de BaseAgent
            signal = super().generate_signal(df, asset=self.focus_asset, model_name=model_name, model_provider=model_provider)
            signals.setdefault("Brian Armstrong", {})[ticker] = signal
            signals_generated = True

        if not signals_generated:
            pass  # Silently skip if no signals are generated

        data["analyst_signals"] = signals
        return state