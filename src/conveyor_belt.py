from typing import List
from production import Item
from worker import Worker


class BeltSlot:
    _slot: Item
    _workers: List[Worker]

    def __init__(self, workers: List[Worker]):
        self._slot = Item.NOTHING
        self._workers = workers

    def work(self):
        indcs = self.get_worker_order()
        for i in indcs:
            self._workers[i].work()

    def get_worker_order(self):
        return sorted(
            list(range(len(self._workers))),
            key=lambda i: self._workers[i].get_num_missing_items(),
        )
