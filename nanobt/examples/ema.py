from nanobt.backtesting import Backtesting
from nanobt.trades import TradeHistory, SideOrder
import talib
import pandas as pd

INIT_PORTFOLIO = 1000
class EMAStrategy(Backtesting):
    
    def __init__(self, value_rapid_ema, value_slow_ema):
        super().__init__()
        self.rapid_ema = None
        self.slow_ema = None
        self.vr_ema = value_rapid_ema
        self.vs_ema = value_slow_ema

    def updateIndicators(self):
        self.rapid_ema = talib.SMA(self.candles['close'].values, timeperiod=self.vr_ema)
        self.slow_ema = talib.SMA(self.candles['close'].values, timeperiod=self.vs_ema)

    def next(self):
        self.updateIndicators()
        if not self.position:
            if self.rapid_ema[-1] > self.slow_ema[-1]:
                self.entry(SideOrder.BUY)
            elif self.rapid_ema[-1] < self.slow_ema[-1]:
                self.entry(SideOrder.SELL)
        else:
            if self.rapid_ema[-1] > self.slow_ema[-1]:
                if self.position.side == SideOrder.SELL:
                    self.exit()
            elif self.rapid_ema[-1] < self.slow_ema[-1]:
                if self.position.side == SideOrder.BUY:
                    self.exit()


data = pd.read_csv('./data/binance_BTCUSDT_5m.csv')
data['datetime'] = pd.to_datetime(data['time'], unit='s')
data = data.drop(columns=['time'])

strategy = EMAStrategy(value_rapid_ema=18, value_slow_ema=34)
strategy.setdata(data)
trades = strategy.run()
th = TradeHistory(trades=trades)

print("Init Portfolio: ", INIT_PORTFOLIO)
print("EMA Strategy: ", th.study(cash=INIT_PORTFOLIO, sizer=0.1, commision=0.04, show_plot=True))

