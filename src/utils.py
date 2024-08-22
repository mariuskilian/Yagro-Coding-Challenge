from collections import defaultdict


class Inventory(defaultdict):
    def __setitem__(self, key, value):
        if value == 0:
            # Remove the key if value is 0
            if key in self:
                del self[key]
        else:
            # Use the default behavior for non-zero values
            super().__setitem__(key, value)

    def __missing__(self, _):
        # Use the default factory to handle missing keys
        return self.default_factory()
