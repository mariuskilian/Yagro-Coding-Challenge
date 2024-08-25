from typing import TYPE_CHECKING, List

from items import Component, Item, Product

if TYPE_CHECKING:
    from conveyor_belt import BeltSlot
    from utils import BeltList


def print_default_factory(
    belt: "List[BeltSlot]", belt_items: "BeltList[Item]", item_off: "Item", t: int
):

    item_keys = {
        None: " ",
        Component.A: "A",
        Component.B: "B",
        Product.P1: "P",
    }

    line_break = "===" + ("====") * len(belt)

    l = [
        " | ",
        " | ",
        " | ",
        line_break,
        "-> ",
        line_break,
        " | ",
        " | ",
        " | ",
    ]

    print()
    print("Time Step: " + str(t))

    for i in range(len(belt)):
        w1 = belt[i]._workers[0]
        w2 = belt[i]._workers[1]

        if w1._assembly_eta > 0:
            l[0] += str(w1._assembly_eta)
        elif w1.get_placable_item() != None:
            l[0] += "P"
        else:
            l[0] += " "
        l[0] += " | "

        l[1] += "B" if w1._inventory[Component.B] > 0 else " "
        l[1] += " | "

        l[2] += "A" if w1._inventory[Component.A] > 0 else " "
        l[2] += " | "

        l[4] += item_keys[belt_items[i]] + "   "

        l[6] += "A" if w2._inventory[Component.A] > 0 else " "
        l[6] += " | "

        l[7] += "B" if w2._inventory[Component.B] > 0 else " "
        l[7] += " | "

        if w2._assembly_eta > 0:
            l[8] += str(w2._assembly_eta)
        elif w2.get_placable_item() != None:
            l[8] += "P"
        else:
            l[8] += " "
        l[8] += " | "

    l[4] += "-> " + item_keys[item_off]

    for line in l:
        print(line)

    print()
    print()
    print(line_break + line_break)
    print(line_break + line_break)
    print(line_break + line_break)

    input()
