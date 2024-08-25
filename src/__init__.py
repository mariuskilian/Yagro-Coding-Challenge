from conveyor_belt import ConveyorBelt
from factory import Factories


def run_simulation():
    factory = Factories.create_default_factory()
    cb = ConveyorBelt(15, factory, True)
    for i in range(10000):
        cb.move_belt_forward()


if __name__ == "__main__":
    run_simulation()
