#!/usr/bin/python3
import sys
import os.path
import os


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_help_message():
    print(color.RED + color.BOLD + "About this program: " + color.END)
    print("This program/script splits the particles.star file to individual star files")
    print(color.RED + color.BOLD + "\nSome notes: " + color.END)
    print("The particles.star file must contain rlnImageName or rlnMicrographName field.")
    print("The user needs to provide the names of the images that are stored in the particles.star file")
    print("This program won't recenter the coordinates. You can recenter the coordinates before or after the spliting(add rlnOriginX rlnOriginY).")
    print(color.RED + color.BOLD + "\nUsage: " + color.END)
    print("python3 " + sys.argv[0] +
          " <particles.star> <image_name> [image_names]")
    print(color.RED + color.BOLD + "\nExample of usage: " + color.END)
    print("python3 " +
          sys.argv[0] + " particles_selected_origin0.star slot10*.mrc")
    print()


if len(sys.argv[:]) < 2 or "-h" in sys.argv[:] or "--h" in sys.argv[:] or "--help" in sys.argv[:] or "-help" in sys.argv[:]:
    print_help_message()
    exit(-1)

starfile = sys.argv[1]
micrographs = sys.argv[2:]
with open(starfile, "r") as f:
    lines = f.readlines()

for micrograph in micrographs:
    outputfilename = micrograph.replace(".mrc", "_split.star")
    if os.path.isfile(outputfilename):
        print(outputfilename + " exists. Skipped.")
        continue
    output = open(outputfilename, "w")
    flag = 1
    newlines = []
    print("Remaining particles: " + str(len(lines)))
    for index, line in enumerate(lines):
        if len(line) < 80:
            output.write(line)
            newlines.append(line)
        elif line.find(micrograph) != -1:
            flag = 0
            output.write(line)
        else:
            newlines.append(line)
    lines = newlines
    output.close()
    if flag == 1:
        print("No particles in " + micrograph)
        os.remove(outputfilename)
    else:
        print("Wrote " + outputfilename)
