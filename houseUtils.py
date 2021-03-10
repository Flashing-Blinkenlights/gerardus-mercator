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

from copy import copy
from interfaceUtils import setBlock as sB
from interfaceUtils import getBlock
from random import choice as choice
from time import sleep as sleep

UNITSIZE = 4
UNITHEIGHT = 4
SLEEPTIME = 0
MAXHEIGHT = 1
DEFAULT_POOL = (1, 2)
ORTHFACTORS = ((1, 0), (-1, 0), (0, 1), (0, -1))
DESIGNATIONS = ("sky", "roofing", "masonry") #corresponding index
IGNORABLES  = ("minecraft:air",
                    "minecraft:oak_leaves", "minecraft:sark_oak_leaves",
                    "minecraft:spruce_leaves", "minecraft:birch_leaves",
                    "minecraft:acacia_leaves", "minecraft:jungle_leaves",
                )
LIQUIDS     = ("minecraft:water", "minecraft:lava")
TRANSPARENT = ("glass", "fence", "trapdoor")
WETNESSON   = True
UNWETTABLE  = {"birch_log", "birch_wood"}
WETBLOCKS   = {"birch":"oak", "oak":"spruce", "spruce":"dark_oak",
                "cobblestone":"mossy_cobblestone",
                "stone_bricks":"mossy_stone_bricks"}

def setBlock(x, y, z, block, a="y", f="north", requirepunch=False):
    if block == "-": return
    if requirepunch and getBlock(x, y, z) in IGNORABLES: return

    waterlogged = "false"
    if WETNESSON \
        and getBlock(x, y, z) == "minecraft:water" \
        and block not in UNWETTABLE:
        for original, new in WETBLOCKS.items():
            if original in block:
                block = block.replace(original, new)
                waterlogged = "true"
                break

    fullblocks = ["[axis={axis}, waterlogged="+waterlogged+"]",
                    "[axis={axis}]", "[waterlogged="+waterlogged+"]",
                    "", "_planks"]

    response = " "
    for addon in fullblocks:
        if not response.isnumeric():
            response = sB(x, y, z, (block+addon).format(axis=a, facing=f))
        else: return
    if not response.isnumeric():print("sB: "+response)

class Palette():
    def __init__(self, pillar, joint, lightMat, heavyMat, window,
                    doorMat="spruce",
                    hasStuds=False, hasShutters=(False, True)):
        self.pillar     = pillar
        self.joint      = joint
        self.lightMat   = lightMat
        self.heavyMat   = heavyMat
        self.window     = window
        self.doorMat    = doorMat

        self.hasStuds       = hasStuds
        self.hasShutters    = hasShutters

    def palettify(self, block):
        return block.format(pillar      = self.pillar,
                            joint       = self.joint,
                            lightMat    = self.lightMat,
                            heavyMat    = self.heavyMat,
                            window      = self.window,
                            doorMat     = self.doorMat,
                            axis="{axis}", facing="{facing}")
palettes = {
    "rustic": Palette("spruce_log", "spruce_wood", "spruce", "cobblestone", "glass_pane"),
    "arid": Palette("sandstone", "chiseled_sandstone", "acacia", "smooth_sandstone", "air", "acacia", hasStuds=True, hasShutters=(False, False))
    }

if """Block with layer compositions for blueprints""":
    empty = ("air", "air", "air", "air")
    ignored = ()

    pillar      = ("{pillar}",          "{pillar}",         "{pillar}",         "{joint}")
    heavy_fencepole  = ("{heavyMat}", "{lightMat}_fence", "{lightMat}_fence", "{lightMat}_fence")

    pillar_lamp  = ("{pillar}",          "{pillar}",         "redstone_lamp",    "redstone_block")

    log_lanternpost = ("{lightMat}_log",    "{lightMat}_fence", "lantern")
    fullheavy_lantern = ("{heavyMat}", "air", "air", "lantern[hanging=true]")

    fence       = ("-",                 "{lightMat}_fence")

    beam            = ("-",                 "-",            "-",            "{pillar}")

    light_beam  = ("{lightMat}_slab",   "air",          "air",          "{pillar}")
    lightwall_beam       = ("{lightMat}",        "{lightMat}",   "{lightMat}",   "{pillar}")
    lightceil   = ("-",                 "-",    "-",    "{lightMat}_slab[type=top]")

    light_heavy  = ("{heavyMat}_slab",   "air",  "air",  "{lightMat}_slab[type=top]")

    heavyfloor        = ("{heavyMat}_slab", "air")
    heavy_beam  = ("{heavyMat}_slab",   "air",          "air",          "{pillar}")
    heavyroom      = ("{heavyMat}_slab",   "air",  "air",  "{heavyMat}_slab[type=top]")
    fullheavy_trapdoor = ("{heavyMat}", "air", "air", "{lightMat}_trapdoor[half=top]")
    heavywall           = ("{heavyMat}",        "{heavyMat}",   "{heavyMat}",   "{heavyMat}")
    heavywall_beam = ("{heavyMat}",        "{heavyMat}",   "{heavyMat}",   "{pillar}")
    heavyceil   = ("-",                 "-",    "-",    "{heavyMat}_slab[type=top]")

    cellarwindow      = ("-", "-",        "{heavyMat}_slab[type=top]")
    low_smallwindow   = ("-", "{window}")
    trapdoorwindow    = ("-", "-", "{doorMat}_trapdoor[half=top, open=true, facing={facing}]")

    #light_joint  = ("{lightMat}_slab",   "air",              "air",              "{joint}")
    #heavy_joint  = ("{heavyMat}_slab",   "air",              "air",              "{joint}")
    #lanternpost = ("-",    "{lightMat}_fence", "lantern")
    #raised_lanternpost  = ("-",                 "{lightMat}_log",   "{lightMat}_fence", "lantern")
    #loglamppost     = ("redstone_torch",    "{lightMat}_log",   "redstone_lamp",    "{lightMat}_slab")
    # beam_cleared       = ("-",                 "air",          "air",          "{pillar}")
    # heavywall_beam       = ("{heavyMat}",        "{heavyMat}",   "{heavyMat}",   "{pillar}")
    # lightwall           = ("{lightMat}",        "{lightMat}",   "{lightMat}",   "{lightMat}")
    # lightceil_cleared   = ("-",                 "air",  "air",  "{lightMat}_slab[type=top]")
    # lightroom       = ("{lightMat}_slab",   "air",  "air",  "{lightMat}_slab[type=top]")
    # smallwind_empty  = ("-", "air")
    # longwind        = ("-", "{window}", "{window}")
    # longwind_empty   = ("-", "air",      "air")


class BlueprintClass():
    def __init__(self,
                        outercorner, cojoining, innercorner, surrounded,
                        wall, corridor,
                        room,
                        window
                    ):
        #   posts
        self.outercorner    = outercorner
        self.cojoining      = cojoining
        self.innercorner    = innercorner
        self.surrounded     = surrounded
        #   walls
        self.wall           = wall
        self.corridor       = corridor
        #   rooms
        self.room           = room
        #windows
        self.window         = window

    def modify(self,
            outercorner=None, cojoining=None, innercorner=None, surrounded=None,
                    wall=None, corridor=None,
                    room=None,
                    window=None):
        #   posts
        if outercorner  != None: self.outercorner    = outercorner
        if cojoining    != None: self.cojoining      = cojoining
        if innercorner  != None: self.innercorner    = innercorner
        if surrounded   != None: self.surrounded     = surrounded
        #   walls
        if wall         != None: self.wall           = wall
        if corridor     != None: self.corridor       = corridor
        #   rooms
        if room         != None: self.room           = room
        #windows
        if window       != None: self.window         = window

if """Block with blueprint classes""":
    ignoredClass        = BlueprintClass(*8*[ignored])
    flatroofClass       = BlueprintClass(*3*[heavyfloor], ignored, heavyfloor, *3*[ignored])
    fenceClass          = BlueprintClass(*3*[fence], ignored, fence, *3*[ignored])
    frameClass          = BlueprintClass(*4*[pillar], *2*[beam], *2*[ignored])

    yardClass           = copy(fenceClass)
    yardClass.modify        (*3*[log_lanternpost], ignored, fence)

    lightstiltClass     = copy(frameClass)
    lightstiltClass.modify  (room=lightceil)
    heavystiltClass     = copy(frameClass)
    heavystiltClass.modify  (room=heavyceil)

    lightframeClass     = copy(frameClass)
    lightframeClass.modify  (innercorner=pillar_lamp,
                                wall=lightwall_beam, corridor=beam,
                                room=lightceil, window=low_smallwindow
                            )

    heavyframeClass     = copy(frameClass)
    heavyframeClass.modify  (innercorner=pillar_lamp,
                                wall=heavywall_beam, corridor=heavy_beam,
                                room=heavyroom, window=cellarwindow
                            )

    transitionframeClass    = copy(heavyframeClass)
    transitionframeClass.modify(room=light_heavy)

    aridClass           = BlueprintClass(*2*[heavywall_beam], fullheavy_lantern, heavy_fencepole,
                            heavywall_beam, *2*[fullheavy_trapdoor], trapdoorwindow)

if """Block with blueprint sets""":
    ignored             = len(DESIGNATIONS)*[ignoredClass]
    rusticground   = (ignoredClass, yardClass, transitionframeClass)
    rustic         = (ignoredClass, flatroofClass, lightframeClass)
    aridground                = (ignoredClass, yardClass, aridClass)
    arid                = (ignoredClass, flatroofClass, aridClass)

blueprint_collections = {"rustic": {"ground": rusticground, "regular": rustic},
                            "arid": {"ground": aridground, "regular": arid}
                        }

class Floor():
    def __init__(self, grid, blueprintset=ignored, window=ignored, level=0, max=MAXHEIGHT, pool = DEFAULT_POOL):
        if level >= max: pool = [1]

        ## DEBUG: print()
        ## DEBUG: print(repr(grid).replace("], [", "]\n["))

        self.pool = pool
        self.grid = [[0 for i in range(len(grid[0]))] for j in range(len(grid))]  #layout for the next floor
        self.blueprints = [[None for i in range(len(grid[0]))] for j in range(len(grid))]  #buildable floor
        self.blueprintset = blueprintset
        self.window = window

        for x, row in enumerate(grid):
            for y, item in enumerate(row):
                self.setBlueprints(x, y, item, blueprintset[int(item)])

    def setBlueprints(self, x, y, item, blueprintclass):
        if ispostindex(x, y):
            if item%1 >= 0.3:       self.blueprints[x][y] = blueprintclass.surrounded
            elif item%1 >= 0.2:     self.blueprints[x][y] = blueprintclass.innercorner
            elif item%1 >= 0.1:     self.blueprints[x][y] = blueprintclass.cojoining
            else:                   self.blueprints[x][y] = blueprintclass.outercorner
        elif iswallindex(x, y):
            if item%1 >= 0.1:       self.blueprints[x][y] = blueprintclass.corridor
            else:                   self.blueprints[x][y] = blueprintclass.wall
        elif isroomindex(x, y):
            #extend to include different room types
            if True:                self.blueprints[x][y] = blueprintclass.room
            if int(item) > 1:       self.planroomabove(x, y)
        else: raise Error("Unexpected index values")

    def planroomabove(self, x, y):
        self.grid[x][y] = choice(self.pool)
        for u in range(-1, 2):
            for v in range(-1, 2):

                if [u, v] == [0, 0]:
                    continue

                elif self.grid[x][y] == 1:  #garden/roof
                    if int(self.grid[x+u][y+v]) == 1:
                        self.grid[x+u][y+v] += 0.1
                    elif int(self.grid[x+u][y+v]) < 1:
                        self.grid[x+u][y+v] = 1

                elif self.grid[x][y] == 2:  #generic room
                    if int(self.grid[x+u][y+v]) == 2:
                        self.grid[x+u][y+v] += 0.1
                    elif int(self.grid[x+u][y+v]) < 2:
                        self.grid[x+u][y+v] = 2

        ## DEBUG: print()
        ## DEBUG: print(repr(self.grid).replace("], [", "]\n["))

class House():

    ## TODO: add roadaccessat
    def __init__(self, address, xsize, ysize, theme):
        self.address = address
        self.xsize = (xsize-1)//UNITSIZE
        self.ysize = (ysize-1)//UNITSIZE
        self.xbuffer = (xsize-1)%UNITSIZE
        self.ybuffer = (ysize-1)%UNITSIZE
        self.floors = []
        self.palette = palettes[theme]
        self.blueprint_collection = blueprint_collections[theme]

        self.doors = []
        self.windows = []

        if xsize > UNITSIZE and ysize > UNITSIZE:
            gridrow = self.xsize*2*[2]+[2]
            grid = self.ysize*2*[gridrow]+[gridrow]
            grid = Floor(grid, pool=[1, 2, 2]).grid #throwaway floor for sensible starting layout
        else: print("Impossible size."); grid = [[0]]
        #print("{}x{}: \n{}\n---".format(self.xsize, self.ysize, grid).replace("], [", "],\n["))
        while grid != [[0 for i in range(len(grid[0]))] for j in range(len(grid))]:
            if len(self.floors) == 0:
                self.floors += [Floor(grid, self.blueprint_collection["ground"], self.blueprint_collection["ground"][2].window)]
            else:
                self.floors += [Floor(grid, self.blueprint_collection["regular"], self.blueprint_collection["regular"][2].window, len(self.floors))]
            grid = self.floors[-1].grid


    def build(self, xorig, yorig, zorig):

        xorig = xorig + self.ybuffer//2 + (self.ybuffer%2>0)*choice([0, 1])
        zorig = zorig + self.xbuffer//2 + (self.xbuffer%2>0)*choice([0, 1])

        for floorno, floor in enumerate(self.floors):
            y = yorig + floor2height(floorno)

            # DEBUG: print()
            # DEBUG: print(repr(floor.grid).replace("], [", "]\n[").replace(", ", "\t"))

            self.buildGeometry(xorig, yorig, zorig, floorno, floor)
            for ux, row in enumerate(floor.blueprints):
                for uy, item in enumerate(row):
                    x = xorig + index2coord(ux)
                    z = zorig + index2coord(uy)

                    if iswallindex(ux, uy):
                        if isxwallindex(ux, uy): axis = "x"
                        elif isywallindex(ux, uy): axis = "z"
                        if floorno == 0:
                            item = self.blueprint_collection["ground"][2].window
                            self.punchWindow(x, y, z, item, axis)
                        else:
                            item = self.blueprint_collection["regular"][2].window
                            self.punchWindow(x, y, z, item, axis)

            self.makeNavigable(xorig, yorig, zorig, floorno, floor)

        for floorno, floor in enumerate(self.floors):
            self.decorateWalls(xorig, yorig, zorig, floorno, floor)

    def buildGeometry(self, xorig, yorig, zorig, floorno, floor):   #basic shape and windows
        y = yorig + floor2height(floorno)
        for ux, row in enumerate(floor.blueprints):
            for uy, item in enumerate(row):

                if item != ignored: sleep(SLEEPTIME)

                axis = "y"
                x = xorig + index2coord(ux)
                z = zorig + index2coord(uy)

                if ispostindex(ux, uy):
                    self.placeBlueprint(x, y, z, item)
                elif isroomindex(ux, uy):
                    for dx in range(UNITSIZE-1):
                        for dz in range(UNITSIZE-1):
                            self.placeBlueprint(x+dx, y, z+dz, item)
                elif isywallindex(ux, uy):
                    axis = "z"
                    for dz in range(UNITSIZE-1):
                        self.placeBlueprint(x, y, z+dz, item, axis)
                elif isxwallindex(ux, uy):
                    axis = "x"
                    for dx in range(UNITSIZE-1):
                        self.placeBlueprint(x+dx, y, z, item, axis)
                else:
                    raise Exception("Problem with index identification occured.")

                if iswallindex(ux, uy) and choice([True, False]):
                    self.doors.append((x, y, z, axis))

    def placeBlueprint(self, x, y, z, item, axis="y", facing="north", requirepunch=False):
        for h, block in enumerate(item):
            block = self.palette.palettify(block)
            setBlock(x, y+h, z, block, axis, facing, requirepunch)

    def punchWindow(self, x, y, z, blueprint, axis):
        xorig, yorig, zorig = x, y, z
        x, _, z = getUnitMiddle(x, 0, z, axis)
        factor = findOuterWall(x, y, z)
        if factor == (0, 0):
            input((x, y, z))
        facing = factor2facing(factor)
        # DEBUG: input("{}, {}, {} | {}:\n\t{}".format(x, y, z, axis, blueprint))
        self.placeBlueprint(x, y, z, blueprint, axis, facing, True)
        self.windows.append((xorig, yorig, zorig))

    def makeNavigable(self, xorig, yorig, zorig, floorno, floor):

        #calculate road connection

        #calculate traffic flow/rooms

        #insert doors at selected places
        for door in self.doors:
            self.punchDoor(*door)
        self.doors = []

        #insert ladders to lower floor

    def punchDoor(self, xorig, yorig, zorig, axis):
        x, y, z = xorig, yorig, zorig

        result = findAccessHeight(x, y, z)
        if not result: return
        h, stairsat = result
        y += h

        x, _, z = getUnitMiddle(x, 0, z, axis)
        factor = findOuterWall(x, y, z)
        facing = factor2facing(factor)
        direction = factor2facing(invertfactor(factor))
        if getBlock(x-factor[0], y, z-factor[1]) not in IGNORABLES:
            if getBlock(x-factor[0], y, z-factor[1]) not in IGNORABLES:
                return
            y += 1

        if stairsat != None:
            block = self.palette.palettify("{doorMat}_stairs[facing={facing}]")
            setBlock(x+stairsat[0], y-1, z+stairsat[1], block, f=direction)
        if "fence" in getBlock(x, y, z):
            block = self.palette.palettify("{doorMat}_fence_gate[facing={facing}]")
            setBlock(x, y, z, block, f=facing)
        else:
            block = self.palette.palettify("{doorMat}_door[facing={facing}, half=")
            setBlock(x, y, z, block+"lower]", f=facing, requirepunch=True)
            setBlock(x, y+1, z, block+"upper]", f=facing, requirepunch=True)
        try: self.windows.remove((xorig, yorig, zorig))
        except: pass

    def decorateWalls(self, xorig, yorig, zorig, floorno, floor):
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
                    self.placeStuds(x, y+UNITSIZE-1, z)

    def placeShutters(self, x, y, z, block="{doorMat}"):
        block = self.palette.palettify(block) + "_trapdoor[open=true, facing={facing}]"
        factor = findOuterWall(x, y, z)
        dx, dz = factor
        facing = factor2facing(factor)
        if dx == 0:
            setBlock(x+1, y, z+dz, block, f=facing)
            setBlock(x-1, y, z+dz, block, f=facing)
        elif dz == 0:
            setBlock(x+dx, y, z+1, block, f=facing)
            setBlock(x+dx, y, z-1, block, f=facing)
        else:
            raise Error("Unexpected set of factors")

    def placeStuds(self, x, y, z, amount=UNITSIZE-1):
        if getBlock(x, y, z) in IGNORABLES: return
        factor = findOuterWall(x, y, z)
        facing = factor2facing(factor)
        block = self.palette.palettify("{lightMat}_button[facing={facing}]")
        dx, dz = factor
        px, pz = perpabsfactor(factor)
        for i in range(amount):
            if getBlock(x+dx+i*px, y, z+dz+i*pz) in IGNORABLES:
                setBlock(x+dx+i*px, y, z+dz+i*pz, block, f=facing)

def index2coord(index):
    coord = UNITSIZE*(index//2)
    if index%2 != 0: coord += 1
    return coord
def coord2index(coord):
        index = 2*(coord//UNITSIZE)
        if index%UNITSIZE != 0: coord += 1
        return index
def factor2axis(factor):
    return "z" if factor[0] == 0 else "x"
def factor2facing(factor):
    table = {(1, 0):"east",(-1, 0):"west",(0, 1):"south",(0, -1):"north"}
    return table[factor]
def direction2factor(direction):
    table = {"east":(1, 0),"west":(-1, 0),"south":(0, 1),"north":(0, -1)}
    return table[direction]
def floor2height(floor):
    return UNITHEIGHT*floor

def perpabsfactor(factor):
    return (abs(factor[1]), abs(factor[0]))
def invertfactor(factor):
    return (-factor[0], -factor[1])

def ispostindex(x, y):
    return (True if x%2 == 0 and y%2 == 0 else False)
def isroomindex(x, y):
    return (True if x%2 == 1 and y%2 == 1 else False)
def iswallindex(x, y):
    return isxwallindex(x, y) or isywallindex(x, y)
def isxwallindex(x, y):
    return (True if x%2 == 1 and y%2 == 0 else False)
def isywallindex(x, y):
    return (True if x%2 == 0 and y%2 == 1 else False)

def getUnitMiddle(x=0, y=0, z=0, axis="y"):
    y += UNITHEIGHT//2
    if axis == "x":
        x += (UNITSIZE-1)//2
    elif axis == "z":
        z += (UNITSIZE-1)//2
    return x, y, z
def findAccessHeight(x, y, z):
    check, laststairs = checkFreeSides(x, y, z)
    h = 0
    while check > 1:
        h -= 1
        check, laststairs = checkFreeSides(x, y+h, z)
    while check < 2:
        h += 1
        stairsat = laststairs
        check, laststairs = checkFreeSides(x, y+h, z)
    if stairsat and getBlock(x+stairsat[0], y+h-2, z+stairsat[1]) in IGNORABLES:
        return None
    return h, stairsat

def checkFreeSides(x, y, z, ignoreWater=True):
    sidecount = 0
    lastfree = None
    for dx, dz in ORTHFACTORS:
        if getBlock(x+dx, y, z+dz) in IGNORABLES \
        or (not ignoreWater and getBlock(x+dx, y, z+dz) == "minecraft:water"):
            sidecount += 1
            lastfree = (dx, dz)
    return sidecount, lastfree
def findOuterWall(x, y, z):
    # WARNING: cardinal directions are inverted for ease of use when building walls
    best = [-1, ()]
    for h in range(UNITHEIGHT+1):
        if checkFreeSides(x, y+h, z, False)[0] > 0:
            y += h
            break
    for dx, dz in ORTHFACTORS:
        for h in range(UNITHEIGHT+1):
            block = getBlock(x+dx, y+h, z+dz)
            if block not in IGNORABLES and block not in LIQUIDS:
                if h > best[0]: best = h, (dx, dz)
                break
        else:
            return (dx, dz)
    if best[0] <= 0:
        return (0, 0)
    return best[1]
def findGround(x, z, y=127):
        while getBlock(x, y, z) in IGNORABLES:
            y -= 1
        return y

def getThemes():
    return [name for name in palettes.keys() if name in blueprint_collections.keys()]

# TODO: def placeSign(x, y, z, rotation, text1="", text2="", text3="", text4=""):

#def greenify(x, y, z):
    #y = findGround(x, z, y)
    #setBlock(x, y-1, z, "minecraft:dispenser[facing=up]{Items:[{Slot:0,id:bone_meal,Count:2}]}")
    #interfaceUtils.runCommand("data {} {} {} ")
    #setBlock(x, y-1, z, "dirt")
    #setBlock(x, y-2, z, "dirt")
