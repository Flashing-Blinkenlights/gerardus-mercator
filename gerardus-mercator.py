# ! /usr/bin/python3
"""Generates complex settlements."""
import random

import houseUtils
import interfaceUtils
import mapUtils
from houseUtils import House
from worldLoader import WorldSlice

# x position, z position, x size, z size
area = (0, 0, 64, 64)  # default build area

# Do we send blocks in batches to speed up the generation process?
USE_BATCHING = True

# see if a build area has been specified
# you can set a build area in minecraft using the /setbuildarea command
buildArea = interfaceUtils.requestBuildArea()
if buildArea != -1:
    x1 = buildArea["xFrom"]
    z1 = buildArea["zFrom"]
    x2 = buildArea["xTo"]
    z2 = buildArea["zTo"]
    # print(buildArea)
    area = (x1, z1, x2 - x1, z2 - z1)

print("Build area is at position %s, %s with size %s, %s" % area)

# load the world data
# this uses the /chunks endpoint in the background
worldSlice = WorldSlice(area)
heightmap = worldSlice.heightmaps["MOTION_BLOCKING"]
heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
heightmap = worldSlice.heightmaps["OCEAN_FLOOR"]
heightmap = worldSlice.heightmaps["WORLD_SURFACE"]
# caclulate a heightmap that ignores trees:
heightmap = mapUtils.calcGoodHeightmap(worldSlice)

# show the heightmap as an image
# mapUtils.visualize(heightmap, title="heightmap")

# define a function for easier heightmap access
# heightmap coordinates are not equal to world coordinates!


def heightAt(x, z):
    """Return the height at the appropriate location."""
    return heightmap[(x - area[0], z - area[1])]

# a wrapper function for setting blocks


"""---MAIN---"""

THEMES = houseUtils.getThemes()

counter = 0
while True:
    randx, randz = [random.randint(5, 21), random.randint(5, 21)]
    interfaceUtils.runCommand("fill 9 65 9 33 100 33 air")
    interfaceUtils.runCommand("kill @e[type=item]")
    interfaceUtils.runCommand("fill 9 64 9 33 64 33 dirt")
    interfaceUtils.runCommand("fill 9 63 9 33 63 33 dirt")
    interfaceUtils.runCommand("fill 9 62 9 33 60 33 stone")
    print("House #{}: {}x{}".format(counter, randx, randz))
    interfaceUtils.runCommand(
        "fill 10 64 10 {} 64 {} minecraft:water".format(9 + randx, 9 + randz))
    newHouse = House("House #" + str(counter),
                     randz, randx, random.choice(THEMES)
                     )
    newHouse.build(10, 64, 10)
    input("Done!")
    counter += 1
