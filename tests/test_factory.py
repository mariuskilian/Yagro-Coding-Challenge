import unittest

from blueprint import BlueprintTemplates
from factory import BeltSlot
from items import Component, Product
from utils import Inventory
from worker import Worker


class TestBeltSlot(unittest.TestCase):
    def setUp(self):
        # Ideally mock workers
        blueprint = BlueprintTemplates.create_default_blueprint()
        self.w1, self.w2 = Worker(2, blueprint), Worker(2, blueprint)
        self.belt_slot = BeltSlot([self.w1, self.w2])

    def test_get_worker_priority_order_1(self):
        # Test getting the correct priority list (1/2)
        self.w1._inventory[Component.A] += 1
        self.w1._capacity -= 1
        sorted_order = self.belt_slot.get_worker_order()
        self.assertEqual(sorted_order, [0, 1])

    def test_get_worker_priority_order_2(self):
        # Test getting the correct priority list (2/2)
        self.w2._inventory[Component.A] += 1
        self.w2._capacity -= 1
        sorted_order = self.belt_slot.get_worker_order()
        self.assertEqual(sorted_order, [1, 0])

    def test_work_handled_item(self):
        # Test standard handling of different item types
        handled_item, _ = self.belt_slot.work(None, Inventory())
        self.assertEqual(handled_item, None)

        handled_item, _ = self.belt_slot.work(Component.A, Inventory())
        self.assertEqual(handled_item, None)

        handled_item, _ = self.belt_slot.work(Product.P1, Inventory())
        self.assertEqual(handled_item, Product.P1)

    def test_work_cumulative_requests(self):
        # Test if the same item gets requested by multiple workers, it's tracked properly
        _, requests = self.belt_slot.work(Component.A, Inventory())
        self.assertEqual(len(requests.keys()), 1)
        self.assertEqual(requests[Component.B], 1)

        _, requests = self.belt_slot.work(Component.A, Inventory())
        self.assertEqual(len(requests.keys()), 1)
        self.assertEqual(requests[Component.B], 2)

    def test_work_handled_requests(self):
        # Test if workers start getting their requests filled, that the requests go down
        self.belt_slot.work(Component.A, Inventory())
        _, requests = self.belt_slot.work(Component.A, Inventory())
        self.assertEqual(len(requests.keys()), 1)
        self.assertEqual(requests[Component.B], 2)

        _, requests = self.belt_slot.work(Component.B, Inventory())
        self.assertEqual(len(requests.keys()), 1)
        self.assertEqual(requests[Component.B], 1)

        _, requests = self.belt_slot.work(Component.B, Inventory())
        self.assertEqual(len(requests.keys()), 0)

    def test_work_item_overflow(self):
        # Test if both workers already have the component, that it doesn't get handled
        self.belt_slot.work(Component.A, Inventory())
        self.belt_slot.work(Component.A, Inventory())

        handled_item, requests = self.belt_slot.work(Component.A, Inventory())
        self.assertEqual(handled_item, Component.A)
        self.assertEqual(requests[Component.B], 2)

        handled_item, requests = self.belt_slot.work(Component.A, Inventory())
        self.assertEqual(handled_item, Component.A)
        self.assertEqual(requests[Component.B], 2)

    def test_work_ignore_requested_item(self):
        # Test that workers leave items that are already requested
        handled_item, requests = self.belt_slot.work(
            Component.A, Inventory({Component.A: 1})
        )
        self.assertEqual(handled_item, Component.A)
        self.assertEqual(requests[Component.A], 1)


class TestFactory(unittest.TestCase):
    def setUp(self):
        pass
