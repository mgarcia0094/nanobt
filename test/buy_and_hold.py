import nanobt
import pandas as pd

INIT_PORTFOLIO = 1000

class BuyAndHoldStrategy(nanobt.backtesting.Backtesting):
    def __init__(self):
        super().__init__()
        self.buy_and_hold = False

    def next(self):
        if not self.buy_and_hold:
            self.buy_and_hold = True
            self.buy()

data = pd.read_csv('./data/binance_BTCUSDT_5m.csv')
data['datetime'] = pd.to_datetime(data['time'], unit='s')
data = data.drop(columns=['time'])

strategy = BuyAndHoldStrategy()
strategy.setdata(data)
trades = strategy.run()

th = nanobt.trades.TradeHistory(trades=trades)
print("Init Portfolio: ", INIT_PORTFOLIO)
print("Buy and Hold Strategy: ", th.study(cash=INIT_PORTFOLIO, sizer=1, commision=0.04, show_plot=False))


