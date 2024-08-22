from typing import Dict, List
from enum import Enum, auto


# This enumerable class gives values for each type of item that might be on the
# conveyor belt or in a workers hand.
class Item(Enum):
    NOTHING = 0


class Component(Item):
    A = auto()
    B = auto()


class Product(Item):
    P1 = auto()


class Blueprint:
    _products: List[Product]
    _components: Dict[Item, int]
    _assembly_time: int

    def __init__(
        self, products: List[Product], components: Dict[Item, int], assembly_time: int
    ):
        self._products = products
        self._components = components
        self._assembly_time = assembly_time

    def is_missing_item(self, worker_items, item) -> bool:
        return item in self._components and worker_items[item] < self._components[item]

    def is_ready_to_assemble(self, worker_items) -> bool:
        return all(worker_items[item] >= self._components for item in self._components)

    def get_components(self) -> Dict[Item, int]:
        return self._components

    def get_products(self) -> List[Product]:
        return self._products

    def get_assembly_time(self) -> int:
        return self._assembly_time


class Production:
    @staticmethod
    def create_default_blueprint() -> Blueprint:
        return Blueprint([Item.PRODUCT], {Item.COMP_A: 1, Item.COMP_B: 1}, 4)
