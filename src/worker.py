from utils import Inventory
from production import Item, Product, Component, Blueprint


class Worker:
    # TODO make private
    _capacity: int
    _inventory: Inventory[Item, int]
    _assembly_eta: int
    _blueprint: Blueprint

    def __init__(self, capacity: int, blueprint: Blueprint):
        self._capacity = capacity
        self._inventory = Inventory(int)
        self._assembly_eta = -1
        self._blueprint = blueprint

    # Called exactly once every time step
    # Recieves as input an item (that is currently in front of the worker on the belt),
    # and returns the item type that the worker leaves the slot with after working.
    # E.g. if the worker picks up COMP_A, the slot becomes NOTHING, which is the return
    def work(self, item):
        # Currently assembling product - worker is unavailable to take or palce on belt
        if self.producing > 0:
            self.producing -= 1
            return item
        # Assembly complete
        elif self.producing == 0:
            self.complete_assembly()
        # Worker can place product on conveyor belt
        placable_item = self.get_placable_item()
        if item == Item.NOTHING and placable_item != Item.NOTHING:
            return placable_item
        # Worker handles current item on belt
        elif self._blueprint.is_missing_item(item):
            return Item.NOTHING if self.try_pick_up_item(item) else item
        # If none of the above applied, the worker leaves the slot alone
        return item

    def get_placable_item(self) -> Item:
        for item in self._inventory.keys():
            if isinstance(item, Product):
                return item
        return Item.NOTHING

    def place_item(self, item):
        self._inventory[item] -= 1
        self._capacity += 1

    def try_pick_up_item(self, item) -> bool:
        if self._capacity > 0 and self._blueprint.is_missing_item(item):
            self._inventory[item] += 1
            self.capcity -= 1
            self.check_blueprint_for_assembly()
            return True
        return False

    def check_blueprint_for_assembly(self):
        if self._blueprint.is_ready_to_assemble(self._inventory):
            self._assembly_eta = self._blueprint.get_assembly_time()

    def complete_assembly(self):
        if not self._blueprint.is_ready_to_assemble(self._inventory):
            ValueError("The worker does not have the required components")
        for component, amount in self._blueprint.get_components().items():
            self._inventory[component] -= amount
            capacity += amount
        for product in self._blueprint.get_products():
            self._inventory[product] += 1
            capacity -= 1
        self.producing = -1

    # Worker requests an item if it's the only one missing from allowing assembly
    def request_item(self):
        # TODO
        return
