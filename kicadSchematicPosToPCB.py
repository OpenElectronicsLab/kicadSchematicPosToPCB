#!/usr/bin/python3
import sys
import re

# read in the positions from a schematic file
def readPositionsFromSchematic(filename):
    with open(filename, 'rt') as f:
        positions = {}

        reComponentLabels = re.compile(r"L +(\w+) +(\w+)");
        reComponentPosition = re.compile(r"P +(-?[0-9]+) +(-?[0-9]+)");
        reEndComp = re.compile(r"\$EndComp");
        lastPosition = (0, 0)
        lastRef = 'missing ref'

        # simple hack: save the most recent component label and position
        # we've seen, and then associate the most recent position with the
        # most recent label when we see an end module.
        for line in f:
            match = reComponentLabels.match(line)
            if match:
                lastRef = match.group(2)
            else:
                match = reComponentPosition.match(line)
                if match:
                    lastPosition = (int(match.group(1)), int(match.group(2)))
                else:
                    match = reEndComp.match(line)
                    if match:
                        positions[lastRef] = lastPosition
        return positions

# replace the positions of modules in a brd file with the supplied positions
def applyPositionsToBoard(in_filename, out_filename, positions, onlyMoveIfAtOrigin=True):
    with open(in_filename, 'rt') as f:
        lines = f.readlines()

    reModuleRef = re.compile(r'^\s+\(fp_text reference ([^ ]+).*')
    reModulePosition = re.compile(r'^\s+\(at ([\-\.0-9]+) ([\-\.0-9]+)\)')
    reEndModule = re.compile(r'^  \)')
    lastPositionLineNum = -1
    lastRef = 'missing ref'

    for lineNum, line in zip(range(len(lines)), lines):
        match = reModuleRef.match(line)
        if match:
            lastRef = match.group(1)
        else:
            match = reModulePosition.match(line)
            if match:
                lastPositionLineNum = lineNum
            else:
                match = reEndModule.match(line)
                if match:
                    if lastRef in positions and lastPositionLineNum != -1:
                        match = reModulePosition.match(lines[lastPositionLineNum])

                        if not onlyMoveIfAtOrigin or (match.group(1) == "0" and
                                match.group(2) == "0"):
                            newPos = positions[lastRef]
                            lines[lastPositionLineNum] = "    (at {0} {1})\n".format(
                                newPos[0], newPos[1]
                                )

    with open(out_filename, 'wt') as f:
        f.writelines(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: ")
        print("{0} <schematic file> [<board file> [output file]]".format(sys.argv[0]))
        sys.exit(1);

    sch_filename = sys.argv[1];

    if len(sys.argv) > 2:
        brd_filename = sys.argv[2]
    elif sch_filename[-4:] == ".sch":
        brd_filename = sch_filename[:-4] + ".brd"
    else:
        brd_filename = sch_filename + ".brd"

    if len(sys.argv) > 3:
        out_filename = sys.argv[3]
    else:
        out_filename = brd_filename

    print("{0} + {1} -> {2}".format(sch_filename, brd_filename, out_filename))

    # read in the positions from the schematic
    positions = readPositionsFromSchematic(sch_filename)

    # scale the positions up by a factor of 10 to match the brd file defaults
    schToBrdScale = 0.01
    scaledPositions = dict(zip(positions.keys(),
        map(lambda x: (schToBrdScale*x[0], schToBrdScale*x[1]),
            positions.values())
        ))

    # patch the board file with the new positions
    applyPositionsToBoard(brd_filename, out_filename, scaledPositions)
