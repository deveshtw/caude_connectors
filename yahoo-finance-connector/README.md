# Yahoo Finance Connector

An MCP (Model Context Protocol) server that lets Claude fetch the current
price of a stock, ETF, or crypto ticker using the [`yfinance`](https://pypi.org/project/yfinance/)
Python library.

## Tool

- **`get_ticker_price(symbol)`** — Returns the current price for a ticker
  (e.g. `AAPL`, `MSFT`, `BTC-USD`), along with currency, previous close,
  and change/change-percent when available.

## Setup

```bash
cd yahoo-finance-connector
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run standalone

```bash
python server.py
```

## Connect to Claude Code

```bash
claude mcp add yahoo-finance -- python /absolute/path/to/yahoo-finance-connector/server.py
```

## Connect to Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "yahoo-finance": {
      "command": "python",
      "args": ["/absolute/path/to/yahoo-finance-connector/server.py"]
    }
  }
}
```

Restart Claude Desktop, then ask something like:

> What's the current price of TSLA?
