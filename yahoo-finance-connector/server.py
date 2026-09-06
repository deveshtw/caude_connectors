"""MCP connector exposing Yahoo Finance ticker prices to Claude."""

import requests
import yfinance as yf

try:
    from mcp.server.fastmcp import FastMCP
except ModuleNotFoundError:
    from mcp.server.mcpserver import MCPServer as FastMCP

mcp = FastMCP("yahoo-finance")

# yfinance defaults to a curl_cffi client that impersonates a browser's TLS
# fingerprint. Some network setups (proxies, corporate firewalls) reset that
# connection; a plain requests.Session with a normal User-Agent works there.
_FALLBACK_SESSION = requests.Session()
_FALLBACK_SESSION.headers.update({"User-Agent": "Mozilla/5.0"})


def _fetch_price(symbol: str, session=None):
    """Return (fast_info, price) for symbol, forcing the network fetch now."""
    info = yf.Ticker(symbol, session=session).fast_info
    price = info["last_price"]  # triggers the actual HTTP request
    return info, price


@mcp.tool()
def get_ticker_price(symbol: str) -> dict:
    """Get the current price of a stock/ETF/crypto ticker from Yahoo Finance.

    Args:
        symbol: Ticker symbol, e.g. "AAPL", "MSFT", "BTC-USD".
    """
    symbol = symbol.strip().upper()

    try:
        info, price = _fetch_price(symbol)
    except Exception:
        try:
            info, price = _fetch_price(symbol, session=_FALLBACK_SESSION)
        except Exception as exc:
            raise RuntimeError(
                f"Could not fetch price for ticker '{symbol}' from Yahoo Finance: {exc}"
            ) from exc

    result = {"symbol": symbol, "price": price}

    try:
        currency = info["currency"]
    except Exception:
        currency = None
    try:
        previous_close = info["previous_close"]
    except Exception:
        previous_close = None

    if currency:
        result["currency"] = currency
    if previous_close:
        result["previous_close"] = previous_close
        result["change"] = price - previous_close
        result["change_percent"] = (price - previous_close) / previous_close * 100

    return result


if __name__ == "__main__":
    mcp.run()
