"""
Contains utilities for generating and managing houses

Each house is:
X Composed of multiple horizontally cojoined, vertically stacked 5x4x5 units
/ Lit and windowed
/ Roofed
/ Entirely traversible
O Connected to a road
O Furnished

"""

from random import choice as choice
from time import sleep as sleep

from interfaceUtils import getBlock
from interfaceUtils import setBlock as sB

h = max {abs(current_cell.x – goal.x), abs(current_cell.y – goal.y)}
