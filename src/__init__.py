from factory import Factory
from blueprint import BlueprintTemplates
from items import Component, Product
from metrics import InventoryMetric, MetricsManager


def run_simulation():
    # Register metrics to measure
    metrics_manager = MetricsManager()
    metrics_manager.register_metrics(
        InventoryMetric("ItemsGenerated"), InventoryMetric("ItemsOff")
    )

    # Create factory
    blueprint = BlueprintTemplates.create_default_blueprint()
    factory = Factory(3, blueprint, metrics_manager, False)
    for _ in range(100):
        factory.move_belt_forward()

    print("Simulation complete")

    # Print metrics
    print()
    print("Metrics:")

    items_generated = metrics_manager.get_value("ItemsGenerated")
    a, b = items_generated[Component.A], items_generated[Component.B]
    print(f"  Components Generated\t: {a + b}\t(A: {a}, B: {b})")

    items_off = metrics_manager.get_value("ItemsOff")
    a, b = items_off[Component.A], items_off[Component.B]
    print(f"  Products Produced\t: {items_off[Product.P1]}")
    print(f"  Components Missed\t: {a + b}\t(A: {a}, B: {b})")

    print()


if __name__ == "__main__":
    run_simulation()
