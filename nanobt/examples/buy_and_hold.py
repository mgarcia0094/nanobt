from nanobt.backtesting import Backtesting
from nanobt.trades import TradeHistory, SideOrder
import pandas as pd

INIT_PORTFOLIO = 1000
class BuyAndHoldStrategy(Backtesting):
    def next(self):
        if not self.position:
            self.entry(SideOrder.BUY)

data = pd.read_csv('./data/binance_BTCUSDT_5m.csv')
data['datetime'] = pd.to_datetime(data['time'], unit='s')
data = data.drop(columns=['time'])

strategy = BuyAndHoldStrategy()
strategy.setdata(data)
trades = strategy.run()

th = TradeHistory(trades=trades)
print("Init Portfolio: ", INIT_PORTFOLIO)
print("Buy and Hold Strategy: ", th.study(cash=INIT_PORTFOLIO, sizer=1, commision=0.04, show_plot=False))


