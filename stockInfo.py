import yfinance as yf


def getPrice(ticker):
    if(ticker == "BTC"):
        ticker = "BTC-USD"
    stock = yf.Ticker(ticker)
    data = stock.history()
    last_quote = (data.tail(1)['Close'].iloc[0])
    return last_quote
