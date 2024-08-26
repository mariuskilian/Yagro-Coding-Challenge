from typing import List
from blueprint import Blueprint, Item
from metrics import MetricsManager
from utils import BeltList, Inventory
from worker import Worker


# A single belt slot on the conveyor belt, consisting of the workers at the slot and
# managing the work distribution, such as multiple workers not being able to access the
# same slot in the same time step.
class BeltSlot:
    _workers: List[Worker]

    def __init__(self, workers: List[Worker]):
        self._workers = workers

    # Called once per time step
    def work(self, item: Item, requests: Inventory) -> tuple[Item, Inventory]:
        indcs = self.get_worker_order()
        handled_item = item
        for i in indcs:
            worker = self._workers[i]
            # Once a worker "touched" the belt slot, other workers may no longer do so
            may_handle_item = item == handled_item
            handled_item = worker.work(handled_item, requests, may_handle_item)
            # Add this worker's requests to the list of requests
            for req_item, amount in worker.get_requests().items():
                requests[req_item] += amount
        return handled_item, requests

    # Gets a priority order for the workers of this slot, sorting by least to most
    # items missing in order to start assembly. This assures a worker missing less
    # gets priority over the item, allowing earlier produciton
    def get_worker_order(self) -> List[int]:
        return sorted(
            list(range(len(self._workers))),
            key=lambda i: self._workers[i].get_num_missing_items(),
        )


# The factory managing all the logic of the production and its uptime
class Factory:
    _belt: List[BeltSlot]
    _belt_items: BeltList[Item]
    _length: int
    _blueprint: Blueprint
    _metrics: MetricsManager
    _visualize: bool
    _lifetime: int

    def __init__(
        self,
        belt_length: int,
        blueprint: Blueprint,
        metrics: MetricsManager,
        visualize: bool = False,  # Can be set to true to print visualizer in terminal (press Enter to continue)
    ):
        self._belt_length = belt_length
        self._blueprint = blueprint
        self._metrics = metrics
        self._visualize = visualize
        self._belt = [self.generate_belt_slot() for _ in range(belt_length)]
        self._belt_items = BeltList(belt_length, None)
        self._lifetime = 0

    def generate_belt_slot(self) -> BeltSlot:
        n = self._blueprint.get_n_workers_per_slot()
        return BeltSlot([self.generate_worker() for _ in range(n)])

    def generate_worker(self) -> Worker:
        return Worker(self._blueprint.get_worker_capacity(), self._blueprint)

    # Advances the belt the desired number of steps
    def move_belt_forward(self, steps=1):
        for i in range(steps):
            # Move the items forward one step
            new_item = self._blueprint.generate_item()
            item_off = self._belt_items.advance(new_item)
            # Track the metrics for this movement
            self._metrics.track("ItemsGenerated", new_item)
            self._metrics.track("ItemsOff", item_off)
            # Start tracking requests for this time step. Workers will not take an item
            # if they need it less urgently than someone down the belt who requests it
            requests = Inventory()
            # Iterate through belt backwards to be able to note down requests
            for i in range(len(self._belt) - 1, -1, -1):
                _item, _requests = self._belt[i].work(self._belt_items[i], requests)
                self._belt_items[i] = _item
                # Have to make a copy of requests.items(), since items might get deleted
                # during iteration
                for req_item, amount in list(_requests.items()):
                    if _item in requests:
                        # If the item on the belt is requested, someone is getting their
                        # request fulfilled: remove 1 request
                        requests[req_item] -= 1
                    requests[req_item] += amount
        self._lifetime += steps
        # Visualize
        if self._visualize:
            self._blueprint.print_factory(
                self._belt, self._belt_items, item_off, self._metrics, self._lifetime
            )
