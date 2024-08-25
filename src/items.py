# This enumerable class gives values for each type of item that might be on the
# conveyor belt or in a workers hand.
from enum import Enum, auto


class Item(Enum):
    pass


class Component(Item):
    A = auto()
    B = auto()


class Product(Item):
    P1 = auto()
