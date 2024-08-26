import random
import unittest
from items import Component, Product
from blueprint import BlueprintTemplates


class TestBlueprint(unittest.TestCase):
    def setUp(self):
        # Create a default blueprint instance
        self.blueprint = BlueprintTemplates.create_default_blueprint()

    def test_get_missing_items(self):
        # Test with some worker items
        worker_items = {Component.A: 0, Component.B: 0}
        expected_missing_items = {Component.A: 1, Component.B: 1}
        self.assertEqual(
            self.blueprint.get_missing_items(worker_items), expected_missing_items
        )

    def test_is_missing_item(self):
        # Test cases where items are missing or not missing
        worker_items = {Component.A: 0, Component.B: 1}
        self.assertTrue(self.blueprint.is_missing_item(worker_items, Component.A))
        self.assertFalse(self.blueprint.is_missing_item(worker_items, Component.B))

    def test_is_ready_to_assemble(self):
        # Test with worker items meeting the requirement
        worker_items = {Component.A: 1, Component.B: 1}
        self.assertTrue(self.blueprint.is_ready_to_assemble(worker_items))

        # Test with worker items not meeting the requirement
        worker_items = {Component.A: 0, Component.B: 1}
        self.assertFalse(self.blueprint.is_ready_to_assemble(worker_items))

    def test_get_components(self):
        expected_components = {Component.A: 1, Component.B: 1}
        self.assertEqual(self.blueprint.get_components(), expected_components)

    def test_get_products(self):
        expected_products = [Product.P1]
        self.assertEqual(self.blueprint.get_products(), expected_products)

    def test_generate_item(self):
        # Test that generate_item returns a valid item from the generator list
        generator_items = [None, Component.A, Component.B]
        random.seed(0)  # Set seed for reproducibility
        generated_item = self.blueprint.generate_item()
        self.assertIn(generated_item, generator_items)

    def test_get_n_workers_per_slot(self):
        self.assertEqual(self.blueprint.get_n_workers_per_slot(), 2)

    def test_get_assembly_time(self):
        self.assertEqual(self.blueprint.get_assembly_time(), 4)

    def test_get_worker_capacity(self):
        self.assertEqual(self.blueprint.get_worker_capacity(), 2)


if __name__ == "__main__":
    unittest.main()
