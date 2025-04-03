from src.agents.base_agent import BaseAgent

class CZBinanceAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Changpeng Zhao")
        self.focus_asset = "BNB"  # Default to BNB, Binance’s native token

    def generate_signal(self, data, asset="BNB"):
        return super().generate_signal(data, asset=asset)