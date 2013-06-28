kicadSchematicPosToPCB
======================

Copies component positions from a KiCad schematic file to a board layout.

A complex project in KiCad can contain hundreds of very similar components such
as decoupling capacitors.  Because KiCad piles all of the components together
when you import components from a schematic into a PCB layout, it can be very
tedious to sort these components back out into functionally related groups
before starting on the board layout itself.  This script attempts to simplify
this process by allowing you to move all of the components to the same place on
the PCB layout sheet that they were on the schematic.

Usage
-----

First create your schematic, create your board file, import the netlist from
the schematic, save everything, and exit KiCad.  Then run the script as
follows:

    kicadSchematicPosToPCB.py <schematic file name> <input board file name> <output board file name>

Here `<schematic file name>` is the schematic file to read the component
positions from, `<input board file name>` is the board file you wish to modify,
and `<output board file name>` is the file name with which to save the modified
board file.

If you omit the name of the output board file, the script will default to
overwriting the input board file with the modified version.  If you omit the
names of both board files, the script will substitute the .brd for .sch in the
schematic file name and use that.

Only modules at position 0, 0 will be moved; thus this script should leave
components you've already placed exactly where you placed them.
