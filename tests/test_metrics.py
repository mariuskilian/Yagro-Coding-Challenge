import unittest
from items import Component
from metrics import Metric, MetricsManager, InventoryMetric


class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.test_metric_1 = InventoryMetric("TestMetric1")
        self.test_metric_2 = InventoryMetric("TestMetric2")
        self.mm = MetricsManager()

    def test_initialization(self):
        self.assertEqual(len(self.mm.metrics.keys()), 0)

    def test_registering_one_metric(self):
        self.mm.register_metric(self.test_metric_1)
        self.assertEqual(len(self.mm.metrics.keys()), 1)
        self.assertIsInstance(self.mm.metrics["TestMetric1"], Metric)

    def test_registering_multiple_metrics(self):
        self.mm.register_metrics(self.test_metric_1, self.test_metric_2)
        self.assertEqual(len(self.mm.metrics.keys()), 2)
        self.assertIsInstance(self.mm.metrics["TestMetric1"], Metric)
        self.assertIsInstance(self.mm.metrics["TestMetric2"], Metric)

    def test_get_value(self):
        self.mm.register_metric(self.test_metric_1)
        self.assertEqual(len(self.mm.get_value("TestMetric1").keys()), 0)
        self.mm.track("TestMetric1", Component.A, 5)
        self.assertEqual(len(self.mm.get_value("TestMetric1").keys()), 1)
        self.assertEqual(self.mm.get_value("TestMetric1")[Component.A], 5)

    def test_tracking(self):
        self.mm.register_metric(self.test_metric_1)
        self.mm.track("TestMetric1", Component.A, 5)
        self.assertEqual(len(self.mm.get_value("TestMetric1").keys()), 1)
        self.assertEqual(self.mm.get_value("TestMetric1")[Component.A], 5)


if __name__ == "__main__":
    unittest.main()
