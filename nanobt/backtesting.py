import pandas as pd
from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype
from .trades import Order, Trade, SideOrder

columns_supported = ['datetime', 'open', 'high', 'low', 'close', 'volume']

class Backtesting():

    def __init__(self):
        self.data = None
        self.trades = []
        self.entryorder = None
        self.exitorder = None
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
    
    def savetrade(self):
        if self.entryorder and self.exitorder:
            self.trades.append(Trade(self.entryorder, self.exitorder))
            self.entryorder = None
            self.exitorder = None

    def buy(self):
        price = self.candles['close'][-1]
        if self.entryorder == None:
            self.entryorder = Order(SideOrder.BUY, price)
        else:
            self.exitorder = Order(SideOrder.BUY, price)

        self.savetrade()
        return True

    def sell(self):
        price = self.candles['close'][-1]
        if self.entryorder == None:
            self.entryorder = Order(SideOrder.SELL, price)
        else:
            self.exitorder = Order(SideOrder.SELL, price)

        self.savetrade()
        return True

    def next(self):
        pass

    def run(self):
        assert isinstance(self.data, pd.DataFrame), "DATA MUST BE DATAFRAME"

        for x in range(1, len(self.data)):
            # print(self.data[:x])
            self.candles = pd.DataFrame(self.data[:x])
            self.next()
        
        if self.entryorder:
            if not self.exitorder:
                if self.entryorder.side == SideOrder.BUY:
                    self.exitorder = Order(SideOrder.SELL, self.candles['close'][-1])
                elif self.entryorder.side == SideOrder.SELL:
                    self.exitorder = Order(SideOrder.BUY, self.candles['close'][-1])
                else:
                    raise Exception("RUN SIDE UNKNOWN")
                self.savetrade()
        
        return self.trades

        

    

        
        
        
    
