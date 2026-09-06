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

## Verified example output

```
>>> get_ticker_price("AAPL")
{
  "symbol": "AAPL",
  "price": 319.97,
  "currency": "USD",
  "previous_close": 327.6421,
  "change": -7.67,
  "change_percent": -2.34
}
```

Note: `yfinance` defaults to a `curl_cffi` client that impersonates a
browser's TLS fingerprint; some proxies/firewalls reset that connection.
`server.py` automatically retries with a plain `requests.Session` in that
case, which is what makes the tool work reliably across network setups.
