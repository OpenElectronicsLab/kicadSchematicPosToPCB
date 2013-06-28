#!/usr/bin/python3
import sys
import re

def readPositionsFromSchematic(filename):
    with open(filename, 'rt') as f:
        positions = {}

        reComponentLabels = re.compile(r"L +(\w+) +(\w+)");
        reComponentPosition = re.compile(r"P +([0-9]+) +([0-9]+)");
        reEndComp = re.compile(r"\$EndComp");
        lastPosition = (0, 0)
        lastRef = 'missing ref'

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
    print(readPositionsFromSchematic(sch_filename))
