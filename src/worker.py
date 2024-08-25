from utils import Inventory
from factory import Item, Product, Factory


class Worker:
    _capacity: int
    _inventory: Inventory[Item, int]
    _assembly_eta: int
    _factory: Factory

    def __init__(self, capacity: int, factory: Factory):
        if sum(factory.get_missing_items({}).values()) > capacity:
            ValueError("Worker has less capacity than required for factory")
        self._capacity = capacity
        self._inventory = Inventory(int)
        self._assembly_eta = -1
        self._factory = factory

    # Called exactly once every time step
    # Recieves as input an item (that is currently in front of the worker on the belt),
    # and returns the item type that the worker leaves the slot with after working.
    # E.g. if the worker picks up COMP_A, the slot becomes NOTHING, which is the return
    def work(self, item: Item, requests: Inventory[int], may_handle_item: bool = True):
        # Currently assembling product - worker is unavailable to take or palce on belt
        if self._assembly_eta > 0:
            self._assembly_eta -= 1
            if self._assembly_eta > 0:
                return item
        # Assembly complete
        if self._assembly_eta == 0:
            self.complete_assembly()
        if may_handle_item:
            # Worker can place product on conveyor belt
            if item is None:
                placable_item = self.get_placable_item()
                if placable_item is not None:
                    self.place_item(placable_item)
                    return placable_item
            # Worker handles current item on belt
            if (
                self._factory.is_missing_item(self._inventory, item)
                and self._capacity > 0
            ):
                self.pick_up_item(item)
                return None
            # If none of the above applied, the worker leaves the slot alone
        return item

    def get_placable_item(self) -> Item:
        for item in self._inventory.keys():
            if isinstance(item, Product):
                return item
        return None

    def place_item(self, item: Item):
        self._inventory[item] -= 1
        self._capacity += 1

    def pick_up_item(self, item: Item):
        self._inventory[item] += 1
        self._capacity -= 1
        self.check_factory_for_assembly()

    def check_factory_for_assembly(self):
        if self._factory.is_ready_to_assemble(self._inventory):
            self._assembly_eta = self._factory.get_assembly_time()

    def complete_assembly(self):
        if not self._factory.is_ready_to_assemble(self._inventory):
            ValueError("The worker does not have the required components")
        for component, amount in self._factory.get_components().items():
            self._inventory[component] -= amount
            self._capacity += amount
        for product in self._factory.get_products():
            self._inventory[product] += 1
            self._capacity -= 1
        self._assembly_eta = -1

    def get_num_missing_items(self):
        return sum(self._factory.get_missing_items(self._inventory).values())

    # Worker requests an item if it's the only one missing from allowing assembly
    def get_requests(self):
        missing_items = self._factory.get_missing_items(self._inventory)
        if sum(missing_items.values()) != 1:
            return {}
        return missing_items
