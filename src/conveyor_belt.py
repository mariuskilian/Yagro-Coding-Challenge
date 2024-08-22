from typing import List
from production import Factory, Item, Factories
from utils import BeltList, Inventory
from worker import Worker


class BeltSlot:
    _workers: List[Worker]

    def __init__(self, workers: List[Worker]):
        self._workers = workers

    def work(self, item: Item):
        requests = Inventory(int)
        indcs = self.get_worker_order()
        handled_item = item
        for i in indcs:
            worker = self._workers[i]
            if item == handled_item:
                handled_item = worker.work(item, requests)
            else:
                worker.work(Item.UNAVAILABLE, requests)
            # Add this worker's requests to the list of requests
            for item, amount in worker.get_requests().items():
                requests[item] += amount
        return handled_item, requests

    def get_worker_order(self):
        return sorted(
            list(range(len(self._workers))),
            key=lambda i: self._workers[i].get_num_missing_items(),
        )


class ConveyorBelt:
    _belt: List[BeltSlot]
    _belt_items: BeltList[Item]
    _length: int
    _uptime: int
    _visualize: bool
    _factory: Factory

    def __init__(self, length: int, uptime: int, visualize: bool = False):
        self._length = length
        self._uptime = uptime
        self._visualize = visualize
        self._factory = Factories.create_default_factory()
        self._belt = [self.generate_belt_slot() for _ in range(length)]

    def generate_belt_slot(self) -> BeltSlot:
        n = self._factory.get_n_workers_per_slot()
        return BeltSlot([self.generate_worker() for _ in range(n)])

    def generate_worker(self) -> Worker:
        return Worker(self._factory.get_worker_capacity, self._factory)

    def move_belt_forward(self):
        self._belt_items.advance()
        return

    def get_slot_item(self, idx: int) -> Item:
        return self._belt_items[(self._offset + idx) % self._length]
