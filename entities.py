class Company():
    def __init__(self, name=None, isin=None, ticker=None, nominal=None, market=None, address=None, listed_capital=None):
        self.name = name
        self.isin = isin
        self.ticker = ticker
        self.nominal = nominal
        self.market = market
        self.address = address
        self.listed_capital = listed_capital
    def __str__(self):
        return (f"{self.ticker} - {self.name} - {self.isin} - {self.nominal} - {self.market} - {self.address} - {self.listed_capital}")

class StockValue():
    def __init__(self, isin, last=None, diff=None, max=None, min=None, volume=None, turnover=None, updated=None):
        self.isin = isin
        self.last = last
        self.diff = diff
        self.max = max
        self.min = min
        self.volume = volume
        self.turnover = turnover
        self.updated = updated
        
    def __str__(self):
        return (f"{self.isin} - Last:{self.last} - Dif:{self.diff} - Max:{self.max} - Min:{self.min} - Vol:{self.volume} - TurnOver:{self.turnover} - Updated:{self.updated}")