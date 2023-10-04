import yfinance as yf


def option_chain(ticker):
    """
    :param ticker: Ticker symbol
    :return: Option data
    """
    data = yf.Ticker(ticker)
    # Get beta
    try:
        beta = data.info['beta']
    except KeyError:
        print(f"Could not find beta for {ticker}, warning: using beta = 1")
        beta = 1
    price = data.fast_info["lastPrice"]
    dates = data.options
    calls = []
    puts = []
    for date in dates:
        calls.append(data.option_chain(date).calls)
        puts.append(data.option_chain(date).puts)
    
    return calls, puts, beta, price


if __name__ == "__main__":
    calls, puts, beta, price = option_chain("AAPL")
    print(calls)
    print(puts)
    print(beta)
    print(price)