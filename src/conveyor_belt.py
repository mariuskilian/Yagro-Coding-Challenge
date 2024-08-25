from typing import List
from factory import Factory, Item
from utils import BeltList, Inventory
from worker import Worker


class BeltSlot:
    _workers: List[Worker]

    def __init__(self, workers: List[Worker]):
        self._workers = workers

    def work(self, item: Item, requests: Inventory[int]) -> tuple[Item, Inventory[int]]:
        requests = Inventory(int)
        indcs = self.get_worker_order()
        handled_item = item
        for i in indcs:
            worker = self._workers[i]
            may_handle_item = item == handled_item
            handled_item = worker.work(handled_item, requests, may_handle_item)
            # Add this worker's requests to the list of requests
            for req_item, amount in worker.get_requests().items():
                requests[req_item] += amount
        return handled_item, requests

    def get_worker_order(self) -> List[int]:
        return sorted(
            list(range(len(self._workers))),
            key=lambda i: self._workers[i].get_num_missing_items(),
        )


class ConveyorBelt:
    _belt: List[BeltSlot]
    _belt_items: BeltList[Item]
    _length: int
    _factory: Factory
    _visualize: bool
    _lifetime: int

    def __init__(self, length: int, factory: Factory, visualize: bool = False):
        self._length = length
        self._visualize = visualize
        self._factory = factory
        self._belt = [self.generate_belt_slot() for _ in range(length)]
        self._belt_items = BeltList(length, None)
        self._lifetime = 0

    def generate_belt_slot(self) -> BeltSlot:
        n = self._factory.get_n_workers_per_slot()
        return BeltSlot([self.generate_worker() for _ in range(n)])

    def generate_worker(self) -> Worker:
        return Worker(self._factory.get_worker_capacity(), self._factory)

    def move_belt_forward(self, steps=1):
        for i in range(steps):
            new_item = self._factory.generate_item()
            item_off = self._belt_items.advance(new_item)
            requests = Inventory(int)
            for i in range(len(self._belt) - 1, -1, -1):
                _item, _requests = self._belt[i].work(self._belt_items[i], requests)
                self._belt_items[i] = _item
                for req_item, amount in _requests.items():
                    if req_item in requests:
                        requests[req_item] -= 1
                    requests[req_item] += amount
        self._lifetime += steps
        if self._visualize:
            self._factory.print_factory(
                self._belt, self._belt_items, item_off, self._lifetime
            )

    def get_slot_item(self, idx: int) -> Item:
        return self._belt_items[(self._offset + idx) % self._length]
