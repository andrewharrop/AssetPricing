import numpy
import math
def cdf(x):
    """
    Cumulative distribution function for the standard normal distribution
    :param x: Value to evaluate
    :return: Cumulative distribution function value
    """
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

# Time in this case is years to maturity
def call(underlying, strike, rate, volatility, time):
    """
    Black-Scholes call option price
    :param underlying: Underlying asset price
    :param strike: Strike price

    """
    d1 = (numpy.log(underlying / strike) + (rate + volatility ** 2 / 2) * time) / (volatility * numpy.sqrt(time))
    d2 = d1 - volatility * numpy.sqrt(time)
    return underlying * numpy.exp(-rate * time) * cdf(d1) - strike * cdf(d2)

def put(underlying, strike, rate, volatility, time):
    """
    Black-Scholes put option price
    :param underlying: Underlying asset price
    :param strike: Strike price
    :param rate: Risk-free rate
    :param volatility: Volatility
    :param time: Time to maturity
    :return: Put option price
    """
    d1 = (numpy.log(underlying / strike) + (rate + volatility ** 2 / 2) * time) / (volatility * numpy.sqrt(time))
    d2 = d1 - volatility * numpy.sqrt(time)
    return strike * numpy.exp(-rate * time) * cdf(-d2) - underlying * cdf(-d1)

def call_div(underlying, strike, rate, dividend, volatility, time):
    """
    Black-Scholes call option price with dividends
    :param underlying: Underlying asset price
    :param strike: Strike price
    :param rate: Risk-free rate
    :param dividend: Dividend yield
    :param volatility: Volatility
    :param time: Time to maturity
    :return: Call option price
    """
    d1 = (numpy.log(underlying / strike) + (rate - dividend + volatility ** 2 / 2) * time) / (volatility * numpy.sqrt(time))
    d2 = d1 - volatility * numpy.sqrt(time)
    return underlying * numpy.exp(-dividend * time) * cdf(d1) - strike * numpy.exp(-rate * time) * cdf(d2)

def put_div(underlying, strike, rate, dividend, volatility, time):
    """
    Black-Scholes put option price with dividends
    :param underlying: Underlying asset price
    :param strike: Strike price
    :param rate: Risk-free rate
    :param dividend: Dividend yield
    :param volatility: Volatility
    :param time: Time to maturity
    :return: Put option price
    """
    d1 = (numpy.log(underlying / strike) + (rate - dividend + volatility ** 2 / 2) * time) / (volatility * numpy.sqrt(time))
    d2 = d1 - volatility * numpy.sqrt(time)
    return strike * numpy.exp(-rate * time) * cdf(-d2) - underlying * numpy.exp(-dividend * time) * cdf(-d1)