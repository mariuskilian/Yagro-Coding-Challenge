import unittest
from items import Component, Product
from blueprint import BlueprintTemplates
from worker import Worker


class TestWorker(unittest.TestCase):
    def setUp(self):
        # Initialize a default blueprint
        self.blueprint = BlueprintTemplates.create_default_blueprint()
        # Initialize a worker with capacity 2
        self.worker = Worker(2, self.blueprint)

    def test_initial_capacity(self):
        # Test that worker's initial capacity is correctly set
        self.assertEqual(self.worker._capacity, 2)

    def test_initial_inventory(self):
        # Test that worker's inventory is initialized empty
        self.assertEqual(self.worker._inventory[Component.A], 0)
        self.assertEqual(self.worker._inventory[Component.B], 0)
        self.assertEqual(self.worker._inventory[Product.P1], 0)

    def test_place_item(self):
        # Test placing an item on the conveyor belt
        self.worker._inventory[Product.P1] = 1
        self.worker.place_item(Product.P1)
        self.assertEqual(self.worker._inventory[Product.P1], 0)
        self.assertEqual(self.worker._capacity, 3)

    def test_work_with_item_none(self):
        # Test the worker's behavior when the item is None and there is a placable item
        self.worker._inventory[Product.P1] = 1
        handled_item = self.worker.work(None, {}, may_handle_item=True)
        self.assertEqual(handled_item, Product.P1)
        self.assertEqual(self.worker._inventory[Product.P1], 0)
        self.assertEqual(self.worker._capacity, 3)

    def test_work_with_item_missing(self):
        # Test the worker's behavior when the item is missing and the worker should pick it up
        self.worker._capacity = 1  # Set capacity to 1 to test picking up
        result = self.worker.work(Component.A, {}, may_handle_item=True)
        self.assertEqual(result, None)
        self.assertEqual(self.worker._inventory[Component.A], 1)
        self.assertEqual(self.worker._capacity, 0)

    def test_work_with_item_not_needed(self):
        # Test worker leaving item alone if not needed
        self.worker._inventory[Component.A] = 1
        self.worker._capacity = 1
        result = self.worker.work(Component.A, {}, may_handle_item=True)
        self.assertEqual(result, Component.A)
        self.assertEqual(self.worker._inventory[Component.A], 1)
        self.assertEqual(self.worker._capacity, 1)

    def test_complete_assembly(self):
        # Test completing assembly when the worker has required components
        self.worker._inventory[Component.A] = 1
        self.worker._inventory[Component.B] = 1
        self.worker._capacity = 0
        self.worker.check_for_assembly()
        self.worker.complete_assembly()
        self.assertEqual(self.worker._inventory[Component.A], 0)
        self.assertEqual(self.worker._inventory[Component.B], 0)
        self.assertEqual(self.worker._inventory[Product.P1], 1)
        self.assertEqual(self.worker._capacity, 1)

    def test_get_num_missing_items(self):
        # Test getting the number of missing items for assembly
        self.worker._inventory[Component.A] = 1
        missing_items = self.worker.get_num_missing_items()
        self.assertEqual(
            missing_items, 1
        )  # Assuming 1 missing item in the default blueprint

    def test_get_requests(self):
        # Test getting item requests when only one item is missing
        self.worker._inventory[Component.A] = 1
        requests = self.worker.get_requests()
        self.assertEqual(
            requests[Component.B], 1
        )  # Assuming Component.B is needed for assembly

    def test_get_placable_success(self):
        # Test getting a placable item from inventory when it exists
        self.worker._inventory[Product.P1] = 1
        item = self.worker.get_placable_item()
        self.assertEqual(item, Product.P1)

    def test_get_placable_fail(self):
        # Test getting a placable item from inventory when it exists
        self.worker._inventory[Component.A] = 1
        item = self.worker.get_placable_item()
        self.assertEqual(item, None)


if __name__ == "__main__":
    unittest.main()
