# Crypto AI Hedge Fund

A crypto AI hedge fund that simulates trading agents and backtests strategies.

## Installation

1. Install Poetry: `curl -sSL https://install.python-poetry.org | python3 -`
2. Install dependencies: `poetry install`
3. Activate the virtual environment: `poetry shell`
4. Create a .env folder containing LLMs API KEY
5. Run the project: `poetry run python src/main.py --tickers BTC,ETH,ADA --initial-cash 100000 --start-date 2024-01-01 --end-date 2025-04-03 --show-reasoning
`
