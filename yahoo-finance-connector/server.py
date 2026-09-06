"""MCP connector exposing Yahoo Finance ticker prices to Claude."""

import yfinance as yf

try:
    from mcp.server.fastmcp import FastMCP
except ModuleNotFoundError:
    from mcp.server.mcpserver import MCPServer as FastMCP

mcp = FastMCP("yahoo-finance")


@mcp.tool()
def get_ticker_price(symbol: str) -> dict:
    """Get the current price of a stock/ETF/crypto ticker from Yahoo Finance.

    Args:
        symbol: Ticker symbol, e.g. "AAPL", "MSFT", "BTC-USD".
    """
    symbol = symbol.strip().upper()
    ticker = yf.Ticker(symbol)

    try:
        info = ticker.fast_info
        price = info["last_price"]
    except Exception:
        info = None
        price = None

    if price is None:
        try:
            history = ticker.history(period="1d")
        except Exception as exc:
            raise RuntimeError(
                f"Could not fetch price for ticker '{symbol}' from Yahoo Finance: {exc}"
            ) from exc
        if history.empty:
            raise ValueError(f"No price data found for ticker '{symbol}'")
        price = float(history["Close"].iloc[-1])

    result = {"symbol": symbol, "price": price}

    if info is not None:
        currency = info.get("currency")
        previous_close = info.get("previous_close")
        if currency:
            result["currency"] = currency
        if previous_close is not None:
            result["previous_close"] = previous_close
            result["change"] = price - previous_close
            if previous_close:
                result["change_percent"] = (price - previous_close) / previous_close * 100

    return result


if __name__ == "__main__":
    mcp.run()
