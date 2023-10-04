import yfinance as yf
import sys
import datetime
sys.path.append('./formulas')
# from blackscholes import call, put
from interest_rates import USTreasury10YrRate
# Todo: add API call to fred to get 10y treasury rates to replate hardcoded risk free rate
RISK_FREE_RATE = USTreasury10YrRate()/100
def yfinance_option(ticker, option):
    """
        :param ticker: String, indicates company ticker on yahoo finance
        :param option: String, the name of the contract with all of the information included

        :purpose: The purpose of this is to return the price of a contract
    """

    print(ticker)
    option = option[len(ticker):]
    year = option[:2]
    month = option[2:4]
    day = option[4:6]
    instr_type = option[6]
    strike = int(option[7:])/1000
    data = yf.Ticker(ticker)
    stock_price = data.fast_info["lastPrice"]
    # Get beta
    beta = data.info['beta']
    if instr_type == 'C':
        calls_ = data.option_chain(f'20{year}-{month}-{day}').calls
        return calls_[calls_['strike'] == strike], beta, stock_price

    else:
        puts_ = data.option_chain(f'20{year}-{month}-{day}').puts
        return puts_[puts_['strike'] == strike], beta, stock_price


def option_parser(name, ticker):
    """
    :param name: contact name
    :param ticker: the yahoo finance ticker
    """
    option = name[len(ticker):]
    year = option[:2]
    month = option[2:4]
    day = option[4:6]
    instr_type = option[6]
    strike = float(option[7:])/1000

    return year, month, day, instr_type, strike

def options_valuation(chain, ticker, call, put):
    calls = chain[0]
    puts = chain[1]
    beta = chain[2] or 1
    price = chain[3]
    calls_table = {}
    for table in calls:
        for index, row in table.iterrows():
            meta = option_parser(row['contractSymbol'], ticker)
            last_price = max(row['lastPrice'], row['ask'])
            year, month, day, instr_type, strike = meta
            time = (datetime.datetime(int(f"20{year}"), int(month), int(day)) - datetime.datetime.now()).days / 365
            if instr_type == 'C':
                if str(year)+str(month)+str(day) not in calls_table:
                    calls_table[str(year)+str(month)+str(day)] = {}
                calls_table[str(year)+str(month)+str(day)][strike] = call(price, strike, RISK_FREE_RATE, beta, time), last_price

    puts_table = {}
    for table in puts:
        for index, row in table.iterrows():
            meta = option_parser(row['contractSymbol'], ticker)
            last_price = max(row['lastPrice'], row['ask'])
            year, month, day, instr_type, strike = meta
            time = (datetime.datetime(int(f"20{year}"), int(month), int(day)) - datetime.datetime.now()).days / 365
            if instr_type == 'P':
                if str(year)+str(month)+str(day) not in puts_table:
                    puts_table[str(year)+str(month)+str(day)] = {}
                puts_table[str(year)+str(month)+str(day)][strike] = put(price, strike, RISK_FREE_RATE, beta, time), last_price

    # Eack key in the tables is "YYMMDD", change this to YYYY-MM-DD
    return calls_table, puts_table