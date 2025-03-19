class Company():
    def __init__(self, name, isin, ticker, nominal, market, admitted_capital, address):
        self.name = name
        self.isin = isin
        self.ticker = ticker
        self.nominal = nominal
        self.market = market
        self.admitted_capital = admitted_capital
        self.address = address
    def __str__(self):
        return (f"{self.ticker}-{self.name} ")

