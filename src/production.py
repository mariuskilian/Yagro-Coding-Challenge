from enum import Enum, auto


# This enumerable class gives values for each type of item that might be on the
# conveyor belt or in a workers hand.
class Items(Enum):
    NOTHING = 0
    COMP_A = auto()
    COMP_B = auto()
    PRODUCT = auto()


class Blueprint:
    def __init__(self, products, components, assembly_time):
        self._products = products
        self._components = components
        self._assembly_time = assembly_time

    def is_missing_item(self, worker_items, item) -> bool:
        return item in self._components and worker_items[item] < self._components[item]

    def is_ready_to_assemble(self, worker_items) -> bool:
        return all(worker_items[item] >= self._components for item in self._components)

    def complete_assembly(self, worker_items) -> Items:
        if not self.is_ready_to_assemble(worker_items):
            ValueError("The worker does not have the required components")
        for component, amount in self._components.items():
            worker_items[component] -= amount
        for product in self._products:
            worker_items[product] += 1


class Production:
    @staticmethod
    def create_default_blueprint() -> Blueprint:
        return Blueprint([Items.PRODUCT], {Items.COMP_A: 1, Items.COMP_B: 1}, 4)
