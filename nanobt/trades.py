from enum import Enum
import numpy as np
import matplotlib.pyplot as plt

class SideOrder(Enum):
    BUY = 1
    SELL = 2

class Order():
    def __init__(self, side, price):
        assert isinstance(side, SideOrder), "ORDER ERROR: SIDE IS NOT SIDEORDER"
        self.price = price
        self.side = side

class Trade():
    def __init__(self, entryorder, exitorder):
        assert entryorder.side != exitorder.side, "TRADE ERROR: SAME SIDE ORDERS"
        self.entry_order = entryorder
        self.exit_order = exitorder

class TradeHistory():
    def __init__(self, trades):
        self.trades = trades
    
    def study(self, cash=1000.0, sizer=1.0, commision=0.0, show_plot=True):
        assert 0 <= commision and commision <= 1, "Comission must be number between 0 and 1"
        assert 0 <= sizer and sizer <= 1, "Sizer must be number between 0 and 1"
        assert 0 < cash, "Cash must be number between 0 and 1"
        
        history_cash = [cash]
        for trade in self.trades:
            amount_order = sizer*cash
            cash -= amount_order
            amount_order -= (amount_order*commision)
            pnl = trade.exit_order.price - trade.entry_order.price
            if trade.entry_order.side == SideOrder.SELL:
                pnl *= -1
            amount_order += pnl
            amount_order -= (amount_order*commision)
            cash += amount_order
            history_cash.append(cash)
        
        if show_plot:
            t = np.arange(0, len(history_cash))
            fig, ax = plt.subplots()
            ax.plot(t, history_cash)
            ax.set(xlabel='time', ylabel='price units',
                title='Portfolio History')
            ax.grid()
            plt.show()

        return cash


