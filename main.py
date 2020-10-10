from backtesting import Backtesting
import pandas as pd

class CustomStrategy(Backtesting):
    def next(self):
        print(self.candles[-1:])

data = pd.read_csv('./binance_BTCUSDT_5m.csv')
data['datetime'] = pd.to_datetime(data['time'], unit='s')
data = data.drop(columns=['time'])

strategy = CustomStrategy()
strategy.setdata(data)
trades = strategy.run()
