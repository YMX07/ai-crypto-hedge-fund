from agents.base_agent import BaseAgent

class VitalikButerinAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Vitalik Buterin")
        self.focus_asset = "ETH"

    def generate_signal(self, data):
        return super().generate_signal(data, asset=self.focus_asset)