import random
from typing import TYPE_CHECKING, Callable, Dict, List
from enum import Enum, auto
from items import Component, Item, Product
from printers import print_default_factory

if TYPE_CHECKING:
    from conveyor_belt import BeltSlot
    from utils import BeltList


class Factory:
    _products: List[Product]
    _components: Dict[Item, int]
    _generator: List[Item]
    _n_workers_per_slot: int
    _worker_capacity: int
    _assembly_time: int
    _printer: Callable

    def __init__(
        self,
        products: List[Product],
        components: Dict[Item, int],
        generator: List[Item],
        n_workers_per_slot: int,
        worker_capacity: int,
        assembly_time: int,
        printer: Callable,
    ):
        self._products = products
        self._components = components
        self._generator = generator
        self._n_workers_per_slot = n_workers_per_slot
        self._worker_capacity = worker_capacity
        self._assembly_time = assembly_time
        self._printer = printer

    def get_missing_items(self, worker_items) -> Dict[Item, int]:
        missing_items = self._components.copy()
        for item, amount in worker_items.items():
            if item in missing_items:
                missing_items[item] -= amount
        return missing_items

    def is_missing_item(self, worker_items, item) -> bool:
        return item in self._components and worker_items[item] < self._components[item]

    def is_ready_to_assemble(self, worker_items) -> bool:
        return all(
            worker_items[item] >= self._components[item] for item in self._components
        )

    def get_components(self) -> Dict[Item, int]:
        return self._components

    def get_products(self) -> List[Product]:
        return self._products

    def generate_item(self) -> Item:
        return random.choice(self._generator)

    def get_n_workers_per_slot(self) -> int:
        return self._n_workers_per_slot

    def get_assembly_time(self) -> int:
        return self._assembly_time

    def get_worker_capacity(self) -> int:
        return self._worker_capacity

    def print_factory(
        self,
        belt: "List[BeltSlot]",
        belt_items: "BeltList[Item]",
        item_off: "Item",
        t: int,
    ):
        self._printer(belt, belt_items, item_off, t)


class Factories:
    @staticmethod
    def create_default_factory() -> Factory:
        return Factory(
            products=[Product.P1],
            components={Component.A: 1, Component.B: 1},
            generator=[None, Component.A, Component.B],
            n_workers_per_slot=2,
            worker_capacity=2,
            assembly_time=4,
            printer=print_default_factory,
        )
