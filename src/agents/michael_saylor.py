from agents.base_agent import BaseAgent

class MichaelSaylorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Michael Saylor")
        self.focus_asset = "BTC"

    def generate_signal(self, data):
        return super().generate_signal(data, asset=self.focus_asset)