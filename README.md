# How to Run

Run the `src/__init__.py` file to execute the code with standard parameters (100 time steps, 3 belt slots, 2 workers per belt slot). Some parameters can be adjusted.

* Time Steps: Either change the range in line 17 to `x`, or add a number `y` in `factory.move_belt_forward()` in line 18. The total number of time steps will be `x*y`
* Visualization: If you want visualization (a simple terminal print out), set the final parameter of the Factory constructor from False to True, line 16. With the established `x` and `y` from the previous point, it will print a visualization every `y` steps. You will need to press Enter to continue the execution after every print.
* Belt Slots: Number of belt slots is the first parameter of the Factory constructor, line 16.
* Workers per Belt Slot: This is determined by the \"Default Blueprint Template\", in `src/blueprint.py`, line 89.
* Capacity per Worker & Assembly Time: Same as previous point.

# Assumptions

* Running Python 3.9 or later
* Workers in one conveyor belt all assemble the same product, and have the same capacity
* Workers are told to prefer to leave a component that they don't need as urgently as someone later down the line, meaning items get produced faster
* Workers are greedy, meaning that if they need an item as urgently as another worker down the line, they will take the item