from enum import Enum

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
