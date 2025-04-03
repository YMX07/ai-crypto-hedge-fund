from src.agents.base_agent import BaseAgent

class ElonMuskAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Elon Musk")
        self.focus_asset = "DOGE"  # Default to Dogecoin

    def generate_signal(self, data, asset="DOGE"):
        return super().generate_signal(data, asset=asset)