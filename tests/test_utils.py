import unittest
from items import Component
from utils import Inventory, BeltList


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()

    def test_init_correct(self):
        # Test empty initialization
        self.assertIsInstance(self.inventory, Inventory)
        self.assertEqual(len(self.inventory.keys()), 0)

    def test_missing_item_not_in_inventory(self):
        # Test that the 'in' and 'not in' operators still function
        self.assertNotIn(Component.A, self.inventory)

    def test_add_element(self):
        # Test adding a new element the standard way
        self.inventory[Component.A] = 5
        self.assertEqual(len(self.inventory.keys()), 1)
        self.assertIn(Component.A, self.inventory)
        self.assertEqual(self.inventory[Component.A], 5)

    def test_add_0_value(self):
        # Test adding an element with value 0 shouldn't be added
        self.inventory[Component.A] = 0
        self.assertEqual(len(self.inventory.keys()), 0)
        self.assertNotIn(Component.A, self.inventory)

    def test_add_implicit_default_value(self):
        # Test adding with default value, by assuming the value already
        # exists, even though it does not, setting a element that does not
        # yet exist
        self.inventory[Component.A] += 5
        self.assertEqual(len(self.inventory.keys()), 1)
        self.assertIn(Component.A, self.inventory)
        self.assertEqual(self.inventory[Component.A], 5)

    def test_compare_missing_item(self):
        # Test getting an element that is not in the dict giving default value
        self.assertEqual(self.inventory[Component.A], int())

    def test_remove_0_value(self):
        # Test adding a value, then subtracting it in 2 steps until it reaches
        # default value 0, where it should be removed
        self.inventory[Component.A] = 5
        self.assertEqual(len(self.inventory.keys()), 1)
        self.assertIn(Component.A, self.inventory)
        self.assertEqual(self.inventory[Component.A], 5)
        self.inventory[Component.A] -= 3
        self.assertEqual(len(self.inventory.keys()), 1)
        self.assertIn(Component.A, self.inventory)
        self.assertEqual(self.inventory[Component.A], 2)
        self.inventory[Component.A] -= 2
        self.assertEqual(len(self.inventory.keys()), 0)
        self.assertNotIn(Component.A, self.inventory)
        self.assertEqual(self.inventory[Component.A], 0)

    def test_init_inventory_from_dict_positive(self):
        # Test initializing from a dictionary
        test_dict = {
            Component.A: 1,
            Component.B: 4,
        }
        inventory = Inventory(test_dict)
        self.assertEqual(len(inventory.keys()), 2)
        self.assertIn(Component.A, inventory)
        self.assertIn(Component.B, inventory)
        self.assertEqual(inventory[Component.A], 1)
        self.assertEqual(inventory[Component.B], 4)

    def test_init_inventory_from_dict_with_0_values(self):
        # Test initializing from a dictionary that includes a 0-value
        test_dict = {
            Component.A: 1,
            Component.B: 0,
        }
        inventory = Inventory(test_dict)
        self.assertEqual(len(inventory.keys()), 1)
        self.assertIn(Component.A, inventory)
        self.assertNotIn(Component.B, inventory)
        self.assertEqual(inventory[Component.A], 1)


class TestBeltList(unittest.TestCase):
    test_length = 3

    def setUp(self):
        self.belt_list = BeltList(self.test_length, int)

    def test_init_correct(self):
        # Test initialization
        self.assertEqual(len(self.belt_list), self.test_length)
        self.assertEqual(self.belt_list.size, self.test_length)
        self.assertEqual(self.belt_list[0], 0)
        self.assertEqual(self.belt_list[1], 0)
        self.assertEqual(self.belt_list[2], 0)
        self.assertEqual(self.belt_list.offset, 0)

    def test_advancing_belt(self):
        # Test advancing the belt 4 times (belt length is 3),
        # to see that overflow is being modularized correctly
        self.belt_list.advance(1)
        self.assertEqual(self.belt_list[0], 1)
        self.assertEqual(self.belt_list[1], 0)
        self.assertEqual(self.belt_list[2], 0)

        self.belt_list.advance(2)
        self.assertEqual(self.belt_list[0], 2)
        self.assertEqual(self.belt_list[1], 1)
        self.assertEqual(self.belt_list[2], 0)

        self.belt_list.advance(3)
        self.assertEqual(self.belt_list[0], 3)
        self.assertEqual(self.belt_list[1], 2)
        self.assertEqual(self.belt_list[2], 1)

        self.belt_list.advance(4)
        self.assertEqual(self.belt_list[0], 4)
        self.assertEqual(self.belt_list[1], 3)
        self.assertEqual(self.belt_list[2], 2)

    def test_removed_value_return(self):
        # Test that the removed value is being returned
        # Make last item in list different value
        self.belt_list[-1] = 1
        print(self.belt_list)
        old_value = self.belt_list.advance(2)
        # See if previously set value was removed and assigned properly
        self.assertEqual(old_value, 1)

    def test_offset(self):
        # Test that the offset value updates correctly
        self.belt_list.advance(1)
        self.assertEqual(self.belt_list.offset, self.test_length - 1)
        self.belt_list.advance(2)
        self.assertEqual(self.belt_list.offset, self.test_length - 2)


if __name__ == "__main__":
    unittest.main()
