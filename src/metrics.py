from abc import ABC, abstractmethod

from utils import Inventory


# A generalized abstract metric class
class Metric(ABC):
    @abstractmethod
    def track(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_value(self):
        pass


# The class handling all metrics, keeping a list and allowing read/write
# through the metrics name
class MetricsManager:
    def __init__(self):
        self.metrics = {}

    def register_metric(self, metric: Metric):
        self.metrics[metric.name] = metric

    def register_metrics(self, *metrics: Metric):
        for metric in metrics:
            self.register_metric(metric)

    def track(self, name: str, *args, **kwargs):
        if name in self.metrics:
            self.metrics[name].track(*args, **kwargs)

    def get_value(self, name: str):
        if name in self.metrics:
            return self.metrics[name].get_value()
        return None


# A specific metric that tracks an inventory, aka counting the occurrence of a list of items
class InventoryMetric(Metric):
    def __init__(self, name: str):
        self.name = name
        self.value = Inventory()

    def track(self, key, added_value: int = 1):
        self.value[key] += added_value

    def get_value(self) -> Inventory:
        return self.value
