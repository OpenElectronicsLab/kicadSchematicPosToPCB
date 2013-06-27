#!/usr/bin/python3
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: ")
        print("{0} <schematic file> [<board file> [output file]]".format(sys.argv[0]))
        sys.exit(1);

    scm_filename = sys.argv[1];

    if len(sys.argv) > 2:
        brd_filename = sys.argv[2]
    elif scm_filename[-4:] == ".sch":
        brd_filename = scm_filename[:-4] + ".brd"
    else:
        brd_filename = scm_filename + ".brd"

    if len(sys.argv) > 3:
        out_filename = sys.argv[3]
    else:
        out_filename = brd_filename

    print("{0} + {1} -> {2}".format(scm_filename, brd_filename, out_filename));
