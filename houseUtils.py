# ! /usr/bin/python3
"""
Contains utilities for generating and managing houses.

Each house is:
X Composed of multiple horizontally cojoined, vertically stacked 5x4x5 units
/ Lit and windowed
/ Roofed
/ Entirely traversible
O Connected to a road
O Furnished

"""

from copy import copy
from random import choice as choice
from time import sleep as sleep

from interfaceUtils import getBlock
from interfaceUtils import setBlock as sB

UNITSIZE = 4
UNITHEIGHT = 4
SLEEPTIME = 0
MAXHEIGHT = 1
DEFAULT_POOL = (1, 2)
ORTHFACTORS = ((1, 0), (-1, 0), (0, 1), (0, -1))
DESIGNATIONS = ("sky", "roofing", "masonry")  # corresponding index
IGNORABLES = ("minecraft:air",
              "minecraft:oak_leaves", "minecraft:sark_oak_leaves",
              "minecraft:spruce_leaves", "minecraft:birch_leaves",
              "minecraft:acacia_leaves", "minecraft:jungle_leaves",
              )
LIQUIDS = ("minecraft:water", "minecraft:lava")
TRANSPARENT = ("glass", "fence", "trapdoor")
WETNESSON = True
UNWETTABLE = {"birch_log", "birch_wood"}
WETBLOCKS = {"birch": "oak", "oak": "spruce", "spruce": "dark_oak",
             "cobblestone": "mossy_cobblestone",
             "stone_bricks": "mossy_stone_bricks"}


def setBlock(x, y, z, block, a="y", f="north", requirepunch=False):
    """Place a block at a defined location."""
    if block == "-":
        return
    if requirepunch and getBlock(x, y, z) in IGNORABLES:
        return

    waterlogged = "false"
    if WETNESSON \
            and getBlock(x, y, z) == "minecraft:water" \
            and block not in UNWETTABLE:
        for original, new in WETBLOCKS.items():
            if original in block:
                block = block.replace(original, new)
                waterlogged = "true"
                break

    fullblocks = ["[axis={axis}, waterlogged=" + waterlogged + "]",
                  "[axis={axis}]", "[waterlogged=" + waterlogged + "]",
                  "", "_planks"]

    response = " "
    for addon in fullblocks:
        if not response.isnumeric():
            response = sB(x, y, z, (block + addon).format(axis=a, facing=f))
        else:
            return
    if not response.isnumeric():
        print("sB: " + response)


class Palette():
    """Holds and manages a palette."""

    def __init__(self, pillar, joint, lightMat, heavyMat, window,
                 doorMat="spruce",
                 hasStuds=False, hasShutters=(False, True)):
        """Initialise pallette with various settings."""
        self.pillar = pillar
        self.joint = joint
        self.lightMat = lightMat
        self.heavyMat = heavyMat
        self.window = window
        self.doorMat = doorMat

        self.hasStuds = hasStuds
        self.hasShutters = hasShutters

    def palettify(self, block):
        """Translate placeholders into the appropriate blocks."""
        return block.format(pillar=self.pillar,
                            joint=self.joint,
                            lightMat=self.lightMat,
                            heavyMat=self.heavyMat,
                            window=self.window,
                            doorMat=self.doorMat,
                            axis="{axis}", facing="{facing}")


palettes = {
    "rustic": Palette("spruce_log", "spruce_wood", "spruce",
                      "cobblestone", "glass_pane"),
    "arid": Palette("sandstone", "chiseled_sandstone", "acacia",
                    "smooth_sandstone", "air", "acacia",
                    hasStuds=True, hasShutters=(False, False))
}

if """Block with layer compositions for blueprints""":
    empty = ("air", "air", "air", "air")
    ignored = ()

    pillar = ("{pillar}",          "{pillar}",
              "{pillar}",         "{joint}")
    heavy_fencepole = ("{heavyMat}", "{lightMat}_fence",
                       "{lightMat}_fence", "{lightMat}_fence")

    pillar_lamp = ("{pillar}",          "{pillar}",
                   "redstone_lamp",    "redstone_block")

    log_lanternpost = ("{lightMat}_log",    "{lightMat}_fence", "lantern")
    fullheavy_lantern = ("{heavyMat}", "air", "air", "lantern[hanging=true]")

    fence = ("-",                 "{lightMat}_fence")

    beam = ("-",                 "-",            "-",            "{pillar}")

    light_beam = ("{lightMat}_slab",   "air",
                  "air",          "{pillar}")
    lightwall_beam = ("{lightMat}",        "{lightMat}",
                      "{lightMat}",   "{pillar}")
    lightceil = ("-",                 "-",    "-",
                 "{lightMat}_slab[type=top]")

    light_heavy = ("{heavyMat}_slab",   "air",  "air",
                   "{lightMat}_slab[type=top]")

    heavyfloor = ("{heavyMat}_slab", "air")
    heavy_beam = ("{heavyMat}_slab",   "air",
                  "air",          "{pillar}")
    heavyroom = ("{heavyMat}_slab",   "air",  "air",
                 "{heavyMat}_slab[type=top]")
    fullheavy_trapdoor = ("{heavyMat}", "air", "air",
                          "{lightMat}_trapdoor[half=top]")
    heavywall = ("{heavyMat}",        "{heavyMat}",
                 "{heavyMat}",   "{heavyMat}")
    heavywall_beam = ("{heavyMat}",        "{heavyMat}",
                      "{heavyMat}",   "{pillar}")
    heavyceil = ("-",                 "-",    "-",
                 "{heavyMat}_slab[type=top]")

    cellarwindow = ("-", "-",        "{heavyMat}_slab[type=top]")
    low_smallwindow = ("-", "{window}")
    trapdoorwindow = (
        "-", "-", "{doorMat}_trapdoor[half=top, open=true, facing={facing}]")

    # light_joint  = ("{lightMat}_slab", "air", "air", "{joint}")
    # heavy_joint  = ("{heavyMat}_slab", "air", "air", "{joint}")
    # lanternpost = ("-", "{lightMat}_fence", "lantern")
    # raised_lanternpost=("-", "{lightMat}_log", "{lightMat}_fence", "lantern")
    # loglamppost = ("redstone_torch", "{lightMat}_log",
    #                "redstone_lamp", "{lightMat}_slab")
    # beam_cleared = ("-", "air", "air", "{pillar}")
    # heavywall_beam = ("{heavyMat}", "{heavyMat}", "{heavyMat}",    pillar}")
    # lightwall = ("{lightMat}", "{lightMat}", "{lightMat}", "{lightMat}")
    # lightceil_cleared   = ("-", "air",  "air",  "{lightMat}_slab[type=top]")
    # lightroom   = ("{lightMat}_slab","air","air","{lightMat}_slab[type=top]")
    # smallwind_empty  = ("-", "air")
    # longwind        = ("-", "{window}", "{window}")
    # longwind_empty   = ("-", "air",      "air")


class BlueprintClass():
    """Contains the 'recipe' for a particular build style."""

    def __init__(self,
                 outercorner, cojoining, innercorner, surrounded,
                 wall, corridor,
                 room,
                 window
                 ):
        """Initialise with various designs for different house parts."""
        #   posts
        self.outercorner = outercorner
        self.cojoining = cojoining
        self.innercorner = innercorner
        self.surrounded = surrounded
        #   walls
        self.wall = wall
        self.corridor = corridor
        #   rooms
        self.room = room
        # windows
        self.window = window

    def modify(self,
               outercorner=None, cojoining=None,
               innercorner=None, surrounded=None,
               wall=None, corridor=None,
               room=None,
               window=None):
        """Adjust the blueprint for variations."""
        #   posts
        if outercorner is not None:
            self.outercorner = outercorner
        if cojoining is not None:
            self.cojoining = cojoining
        if innercorner is not None:
            self.innercorner = innercorner
        if surrounded is not None:
            self.surrounded = surrounded
        #   walls
        if wall is not None:
            self.wall = wall
        if corridor is not None:
            self.corridor = corridor
        #   rooms
        if room is not None:
            self.room = room
        # windows
        if window is not None:
            self.window = window


if """Block with blueprint classes""":
    ignoredClass = BlueprintClass(*8 * [ignored])
    flatroofClass = BlueprintClass(
        *3 * [heavyfloor], ignored, heavyfloor, *3 * [ignored])
    fenceClass = BlueprintClass(*3 * [fence], ignored, fence, *3 * [ignored])
    frameClass = BlueprintClass(*4 * [pillar], *2 * [beam], *2 * [ignored])

    yardClass = copy(fenceClass)
    yardClass.modify(*3 * [log_lanternpost], ignored, fence)

    lightstiltClass = copy(frameClass)
    lightstiltClass.modify(room=lightceil)
    heavystiltClass = copy(frameClass)
    heavystiltClass.modify(room=heavyceil)

    lightframeClass = copy(frameClass)
    lightframeClass.modify(innercorner=pillar_lamp,
                           wall=lightwall_beam, corridor=beam,
                           room=lightceil, window=low_smallwindow
                           )

    heavyframeClass = copy(frameClass)
    heavyframeClass.modify(innercorner=pillar_lamp,
                           wall=heavywall_beam, corridor=heavy_beam,
                           room=heavyroom, window=cellarwindow
                           )

    transitionframeClass = copy(heavyframeClass)
    transitionframeClass.modify(room=light_heavy)

    aridClass = BlueprintClass(*2 * [heavywall_beam], fullheavy_lantern,
                               heavy_fencepole, heavywall_beam,
                               *2 * [fullheavy_trapdoor], trapdoorwindow)

if """Block with blueprint sets""":
    ignored = len(DESIGNATIONS) * [ignoredClass]
    rusticground = (ignoredClass, yardClass, transitionframeClass)
    rustic = (ignoredClass, flatroofClass, lightframeClass)
    aridground = (ignoredClass, yardClass, aridClass)
    arid = (ignoredClass, flatroofClass, aridClass)

blueprint_collections = {"rustic": {"ground": rusticground, "regular": rustic},
                         "arid": {"ground": aridground, "regular": arid}
                         }


class Floor():
    """Contains data and methods for generating a floor of a building."""

    def __init__(self, grid, blueprintset=ignored, window=ignored,
                 level=0, max=MAXHEIGHT, pool=DEFAULT_POOL):
        """Initialise with particular settings for instructing construction."""
        if level >= max:
            pool = [1]

        self.pool = pool
        self.grid = [[0 for i in range(len(grid[0]))] for j in range(
            len(grid))]  # layout for the next floor
        self.blueprints = [[None for i in range(len(grid[0]))] for j in range(
            len(grid))]  # buildable floor
        self.blueprintset = blueprintset
        self.window = window

        for x, row in enumerate(grid):
            for y, item in enumerate(row):
                self.setBlueprints(x, y, item, blueprintset[int(item)])

    def setBlueprints(self, x, y, item, blueprintclass):
        """Places appropriate blueprint in container."""
        if ispostindex(x, y):
            if item % 1 >= 0.3:
                self.blueprints[x][y] = blueprintclass.surrounded
            elif item % 1 >= 0.2:
                self.blueprints[x][y] = blueprintclass.innercorner
            elif item % 1 >= 0.1:
                self.blueprints[x][y] = blueprintclass.cojoining
            else:
                self.blueprints[x][y] = blueprintclass.outercorner
        elif iswallindex(x, y):
            if item % 1 >= 0.1:
                self.blueprints[x][y] = blueprintclass.corridor
            else:
                self.blueprints[x][y] = blueprintclass.wall
        elif isroomindex(x, y):
            # extend to include different room types
            if True:
                self.blueprints[x][y] = blueprintclass.room
            if int(item) > 1:
                self.planroomabove(x, y)
        else:
            raise Exception("Unexpected index values")

    def planroomabove(self, x, y):
        """Plan the floor layout above."""
        self.grid[x][y] = choice(self.pool)
        for u in range(-1, 2):
            for v in range(-1, 2):

                if [u, v] == [0, 0]:
                    continue

                elif self.grid[x][y] == 1:  # garden/roof
                    if int(self.grid[x + u][y + v]) == 1:
                        self.grid[x + u][y + v] += 0.1
                    elif int(self.grid[x + u][y + v]) < 1:
                        self.grid[x + u][y + v] = 1

                elif self.grid[x][y] == 2:  # generic room
                    if int(self.grid[x + u][y + v]) == 2:
                        self.grid[x + u][y + v] += 0.1
                    elif int(self.grid[x + u][y + v]) < 2:
                        self.grid[x + u][y + v] = 2


class House():
    """Contains data and functions for building houses."""

    # TODO: add roadaccessat
    def __init__(self, address, xsize, ysize, theme):
        """Initialise with position, size and theme."""
        self.address = address
        self.xsize = (xsize - 1) // UNITSIZE
        self.ysize = (ysize - 1) // UNITSIZE
        self.xbuffer = (xsize - 1) % UNITSIZE
        self.ybuffer = (ysize - 1) % UNITSIZE
        self.floors = []
        self.palette = palettes[theme]
        self.blueprint_collection = blueprint_collections[theme]

        self.doors = []
        self.windows = []

        if xsize > UNITSIZE and ysize > UNITSIZE:
            gridrow = self.xsize * 2 * [2] + [2]
            grid = self.ysize * 2 * [gridrow] + [gridrow]
            # throwaway floor for sensible starting layout
            grid = Floor(grid, pool=[1, 2, 2]).grid
        else:
            print("Impossible size.")
            grid = [[0]]
        while grid != [[0 for i in range(len(grid[0]))]
                       for j in range(len(grid))]:
            if len(self.floors) == 0:
                self.floors += [
                    Floor(grid, self.blueprint_collection["ground"],
                          self.blueprint_collection["ground"][2].window)
                ]
            else:
                self.floors += [
                    Floor(grid, self.blueprint_collection["regular"],
                          self.blueprint_collection["regular"][2].window,
                          len(self.floors))
                ]
            grid = self.floors[-1].grid

    def build(self, xorig, yorig, zorig):
        """Construct the building floor by floor."""
        xorig = xorig + self.ybuffer // 2 + \
            (self.ybuffer % 2 > 0) * choice([0, 1])
        zorig = zorig + self.xbuffer // 2 + \
            (self.xbuffer % 2 > 0) * choice([0, 1])

        for floorno, floor in enumerate(self.floors):
            y = yorig + floor2height(floorno)

            self.buildGeometry(xorig, yorig, zorig, floorno, floor)
            for ux, row in enumerate(floor.blueprints):
                for uy, item in enumerate(row):
                    x = xorig + index2coord(ux)
                    z = zorig + index2coord(uy)

                    if iswallindex(ux, uy):
                        if isxwallindex(ux, uy):
                            axis = "x"
                        elif isywallindex(ux, uy):
                            axis = "z"
                        if floorno == 0:
                            item = self.blueprint_collection["ground"][2] \
                                .window
                            self.punchWindow(x, y, z, item, axis)
                        else:
                            item = self.blueprint_collection["regular"][2] \
                                .window
                            self.punchWindow(x, y, z, item, axis)

            self.makeNavigable(xorig, yorig, zorig, floorno, floor)

        for floorno, floor in enumerate(self.floors):
            self.decorateWalls(xorig, yorig, zorig, floorno, floor)

    def buildGeometry(self, xorig, yorig, zorig, floorno, floor):
        """Build the basic geometry of the house."""
        y = yorig + floor2height(floorno)
        for ux, row in enumerate(floor.blueprints):
            for uy, item in enumerate(row):

                if item != ignored:
                    sleep(SLEEPTIME)

                axis = "y"
                x = xorig + index2coord(ux)
                z = zorig + index2coord(uy)

                if ispostindex(ux, uy):
                    self.placeBlueprint(x, y, z, item)
                elif isroomindex(ux, uy):
                    for dx in range(UNITSIZE - 1):
                        for dz in range(UNITSIZE - 1):
                            self.placeBlueprint(x + dx, y, z + dz, item)
                elif isywallindex(ux, uy):
                    axis = "z"
                    for dz in range(UNITSIZE - 1):
                        self.placeBlueprint(x, y, z + dz, item, axis)
                elif isxwallindex(ux, uy):
                    axis = "x"
                    for dx in range(UNITSIZE - 1):
                        self.placeBlueprint(x + dx, y, z, item, axis)
                else:
                    raise Exception(
                        "Problem with index identification occured.")

                if iswallindex(ux, uy) and choice([True, False]):
                    self.doors.append((x, y, z, axis))

    def placeBlueprint(self, x, y, z, item,
                       axis="y", facing="north", requirepunch=False):
        """Place blocks according to blueprint."""
        for h, block in enumerate(item):
            block = self.palette.palettify(block)
            setBlock(x, y + h, z, block, axis, facing, requirepunch)

    def punchWindow(self, x, y, z, blueprint, axis):
        """Remove part of a wall to create a window."""
        xorig, yorig, zorig = x, y, z
        x, _, z = getWallMiddle(x, 0, z, axis)
        factor = findOuterWall(x, y, z)
        if factor == (0, 0):
            input((x, y, z))
        facing = factor2facing(factor)
        self.placeBlueprint(x, y, z, blueprint, axis, facing, True)
        self.windows.append((xorig, yorig, zorig))

    def makeNavigable(self, xorig, yorig, zorig, floorno, floor):
        """Calculate navigable areas and connect them."""
        # calculate road connection

        # calculate traffic flow/rooms

        # insert doors at selected places
        for door in self.doors:
            self.punchDoor(*door)
        self.doors = []

        # insert ladders to lower floor

    def punchDoor(self, xorig, yorig, zorig, axis):
        """Remove part of a wall to create a door."""
        x, y, z = xorig, yorig, zorig

        result = findAccessHeight(x, y, z)
        if not result:
            return
        h, stairsat = result
        y += h

        x, _, z = getWallMiddle(x, 0, z, axis)
        factor = findOuterWall(x, y, z)
        facing = factor2facing(factor)
        direction = factor2facing(invertfactor(factor))
        if getBlock(x - factor[0], y, z - factor[1]) not in IGNORABLES:
            if getBlock(x - factor[0], y, z - factor[1]) not in IGNORABLES:
                return
            y += 1

        if stairsat is not None:
            block = self.palette.palettify("{doorMat}_stairs[facing={facing}]")
            setBlock(x + stairsat[0], y - 1, z + stairsat[1],
                     block, f=direction)
        if "fence" in getBlock(x, y, z):
            block = self.palette.palettify(
                "{doorMat}_fence_gate[facing={facing}]")
            setBlock(x, y, z, block, f=facing)
        else:
            block = self.palette.palettify(
                "{doorMat}_door[facing={facing}, half=")
            setBlock(x, y, z, block + "lower]", f=facing, requirepunch=True)
            setBlock(x, y + 1, z, block + "upper]",
                     f=facing, requirepunch=True)
        try:
            self.windows.remove((xorig, yorig, zorig))
        except ValueError:
            pass

    def decorateWalls(self, xorig, yorig, zorig, floorno, floor):
        """Add decorative elements to walls."""
        y = yorig + floor2height(floorno)

        for window in self.windows:
            if (floorno <= 0 and self.palette.hasShutters[0]) or \
                    (floorno > 0 and self.palette.hasShutters[0]):
                self.placeShutters(*window)
        self.windows = []

        for ux, row in enumerate(floor.blueprints):
            for uy, item in enumerate(row):
                x = xorig + index2coord(ux)
                z = zorig + index2coord(uy)

                if self.palette.hasStuds and iswallindex(ux, uy):
                    self.placeStuds(x, y + UNITSIZE - 1, z)

    def placeShutters(self, x, y, z, block="{doorMat}"):
        """Places single-height shutters at the appropriate points."""
        block = self.palette.palettify(
            block) + "_trapdoor[open=true, facing={facing}]"
        factor = findOuterWall(x, y, z)
        dx, dz = factor
        facing = factor2facing(factor)
        if dx == 0:
            setBlock(x + 1, y, z + dz, block, f=facing)
            setBlock(x - 1, y, z + dz, block, f=facing)
        elif dz == 0:
            setBlock(x + dx, y, z + 1, block, f=facing)
            setBlock(x + dx, y, z - 1, block, f=facing)
        else:
            raise Exception("Unexpected set of factors")

    def placeStuds(self, x, y, z, amount=UNITSIZE - 1):
        """Place decorative studs at the appropriate position."""
        if getBlock(x, y, z) in IGNORABLES:
            return
        factor = findOuterWall(x, y, z)
        facing = factor2facing(factor)
        block = self.palette.palettify("{lightMat}_button[facing={facing}]")
        dx, dz = factor
        px, pz = perpabsfactor(factor)
        for i in range(amount):
            if getBlock(x + dx + i * px, y, z + dz + i * pz) in IGNORABLES:
                setBlock(x + dx + i * px, y, z + dz + i * pz, block, f=facing)


def index2coord(index):
    """Translate grid index into local coordinate value."""
    coord = UNITSIZE * (index // 2)
    if index % 2 != 0:
        coord += 1
    return coord


def coord2index(coord):
    """Translate local coordinate value into grid index."""
    index = 2 * (coord // UNITSIZE)
    if index % UNITSIZE != 0:
        coord += 1
    return index


def factor2axis(factor):
    """Convert directional factors to an axis."""
    return "z" if factor[0] == 0 else "x"


def factor2facing(factor):
    """Convert directional factors to a cardinal direction."""
    table = {(1, 0): "east", (-1, 0): "west",
             (0, 1): "south", (0, -1): "north"}
    return table[factor]


def direction2factor(direction):
    """Convert cardinal direction to directional factor."""
    table = {"east": (1, 0), "west": (-1, 0),
             "south": (0, 1), "north": (0, -1)}
    return table[direction]


def floor2height(floor):
    """Convert floor number to block height."""
    return UNITHEIGHT * floor


def perpabsfactor(factor):
    """Convert factor into the perpendicular absolute factor."""
    return (abs(factor[1]), abs(factor[0]))


def invertfactor(factor):
    """Invert a factor."""
    return (-factor[0], -factor[1])


def ispostindex(x, y):
    """Examine whether index is a post location."""
    return (True if x % 2 == 0 and y % 2 == 0 else False)


def isroomindex(x, y):
    """Examine whether index is a room location."""
    return (True if x % 2 == 1 and y % 2 == 1 else False)


def iswallindex(x, y):
    """Examine whether index is a wall location."""
    return isxwallindex(x, y) or isywallindex(x, y)


def isxwallindex(x, y):
    """Examine whether index is a wall location along the X-axis."""
    return (True if x % 2 == 1 and y % 2 == 0 else False)


def isywallindex(x, y):
    """Examine whether index is a wall location along the Y-axis."""
    return (True if x % 2 == 0 and y % 2 == 1 else False)


def getWallMiddle(x=0, y=0, z=0, axis="y"):
    """Return the center coordinates of a wall."""
    y += UNITHEIGHT // 2
    if axis == "x":
        x += (UNITSIZE - 1) // 2
    elif axis == "z":
        z += (UNITSIZE - 1) // 2
    return x, y, z


def findAccessHeight(x, y, z):
    """Discover the ideal position for a door."""
    check, laststairs = checkFreeSides(x, y, z)
    h = 0
    while check > 1:
        h -= 1
        check, laststairs = checkFreeSides(x, y + h, z)
    while check < 2:
        h += 1
        stairsat = laststairs
        check, laststairs = checkFreeSides(x, y + h, z)
    if (stairsat and getBlock(x + stairsat[0], y + h - 2, z + stairsat[1])
            in IGNORABLES):
        return None
    return h, stairsat


def checkFreeSides(x, y, z, ignoreWater=True):
    """Determine which side is the most accessible."""
    sidecount = 0
    lastfree = None
    for dx, dz in ORTHFACTORS:
        if getBlock(x + dx, y, z + dz) in IGNORABLES \
                or (not ignoreWater
                    and getBlock(x + dx, y, z + dz) == "minecraft:water"):
            sidecount += 1
            lastfree = (dx, dz)
    return sidecount, lastfree


def findOuterWall(x, y, z):
    """Determine the directional factor towards the outside of a wall."""
    # WARNING: cardinal directions are inverted for ease of use
    best = [-1, ()]
    for h in range(UNITHEIGHT + 1):
        if checkFreeSides(x, y + h, z, False)[0] > 0:
            y += h
            break
    for dx, dz in ORTHFACTORS:
        for h in range(UNITHEIGHT + 1):
            block = getBlock(x + dx, y + h, z + dz)
            if block not in IGNORABLES and block not in LIQUIDS:
                if h > best[0]:
                    best = h, (dx, dz)
                break
        else:
            return (dx, dz)
    if best[0] <= 0:
        return (0, 0)
    return best[1]


def findGround(x, z, y=127):
    """Determine the ground height (works in caves)."""
    while getBlock(x, y, z) in IGNORABLES:
        y -= 1
    return y


def getThemes():
    """Return all themes."""
    return [name for name in palettes.keys()
            if name in blueprint_collections.keys()]

# TODO: def placeSign(x, y, z, rotation, text1="", text2="", ...):

# TODO: def greenify(x, y, z):
