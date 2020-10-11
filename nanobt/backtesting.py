import pandas as pd
from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype
from .trades import Order, Trade, SideOrder

columns_supported = ['datetime', 'open', 'high', 'low', 'close', 'volume']

class Backtesting():

    def __init__(self):
        self.data = None
        self.trades = []
        self.position = None
        self.candles = None

    def setdata(self, data):
        assert isinstance(data, pd.DataFrame), "DATA must be instance of pandas Dataframe"
        assert set(columns_supported).issubset(data.columns), "data columns must be ['datetime', 'open', 'high', 'low', 'close', 'volume']"
        
        assert is_datetime64_any_dtype(data['datetime']), "Datetime Column not is datetime64"
        assert is_numeric_dtype(data['open']), "Open Column not is numeric"
        assert is_numeric_dtype(data['high']), "High Column not is numeric"
        assert is_numeric_dtype(data['low']), "Low Column not is numeric"
        assert is_numeric_dtype(data['close']), "Close Column not is numeric"
        assert is_numeric_dtype(data['volume']), "Volume Column not is numeric"

        data.sort_values(by=['datetime'], inplace=True)
        data.set_index('datetime', inplace=True)

        self.data = data
    
    def setdatafromcsv(self, path):
        self.setdata(pd.read_csv(path))

    def entry(self, typePosition):
        assert typePosition == SideOrder.BUY or typePosition == SideOrder.SELL, "Incorrect Side"
        assert not self.position, "ERROR ENTRY POSITION" # ya habia posición abierta
        price = self.candles['close'][-1]
        self.position = Order(typePosition, price)

    def exit(self):
        assert self.position, "ERROR EXIT POSITION" # NO habia posición abierta
        typePosition = SideOrder.BUY if self.position.side == SideOrder.SELL else SideOrder.SELL
        price = self.candles['close'][-1]
        self.trades.append(Trade(self.position, Order(typePosition, price)))
        self.position = None

    def next(self):
        pass

    def run(self):
        assert isinstance(self.data, pd.DataFrame), "DATA MUST BE DATAFRAME"

        for x in range(1, len(self.data)):
            self.candles = pd.DataFrame(self.data[:x])
            self.next()
        
        if self.position:
            self.exit()
        
        return self.trades

        

    

        
        
        
    
