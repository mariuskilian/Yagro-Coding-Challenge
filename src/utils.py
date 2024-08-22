from collections import defaultdict


class Inventory(defaultdict):
    def __setitem__(self, key, value):
        if value == 0:
            # Remove the key if value is 0
            if key in self:
                del self[key]
        else:
            # Use default behaviour
            super().__setitem__(key, value)


class BeltList(list):
    def __init__(self, size, default_element):
        super().__init__([default_element] * size)
        self.size = size
        self.offset = 0

    def advance(self, new_value):
        old_value = self[self.offset]
        self[self.offset] = new_value
        self.offset = (self.offset + 1) % self.size
        return old_value

    def __getitem__(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        # Calculate the index in the circular list based on the current offset
        return super().__getitem__((self.offset + index) % self.size)
