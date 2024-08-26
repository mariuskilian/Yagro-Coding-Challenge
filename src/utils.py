from collections import defaultdict


# A default dictionary with int factory that sets missing keys values to 0
# and removes keys whose value is set to 0
class Inventory(defaultdict):

    def __init__(self, initial_dict=None):
        super().__init__(int)

        if initial_dict:
            for key, value in initial_dict.items():
                if value != 0:
                    self[key] = value

    def __setitem__(self, key, value):
        if value == 0:
            if key in self:
                del self[key]
        else:
            super().__setitem__(key, value)


# A belt list, that allows adding a new item to the front of the list, removing
# the item at the back of the list. This 'advancing' of the belt is an O(1) operation,
# as is accessing any item in the list
class BeltList(list):

    def __init__(self, size, default_element_factory):
        super().__init__([default_element_factory() for _ in range(size)])
        self.size = size
        self.offset = 0

    # Adds new_value to "front" of list, replacing value at the "end" of list
    def advance(self, new_value):
        self.offset = (self.offset - 1) % self.size
        old_value = super().__getitem__(self.offset)
        super().__setitem__(self.offset, new_value)
        return old_value

    # Calculate the index in the circular list based on the current offset
    def _get_real_index(self, index):
        return (self.offset + index) % self.size

    def __getitem__(self, index):
        if index <= -self.size or index >= self.size:
            raise IndexError("Index out of range")
        return super().__getitem__(self._get_real_index(index))

    def __setitem__(self, index, value):
        if index <= -self.size or index >= self.size:
            raise IndexError("Index out of range")
        super().__setitem__(self._get_real_index(index), value)
