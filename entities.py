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

