#!/usr/bin/python3

import sys
import os
import math
segment_num = 20
txtfiles = sys.argv[1:]


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


if len(sys.argv[:]) == 1:
    print()
    print(color.RED + color.BOLD + "About this program: " + color.END)
    print("This program will further split the segments into smaller segments. Each segment will have 20 coordinates.")

    print(color.GREEN + color.BOLD + "Arguments: " + color.END)
    print(
        "python3 split_segments.py <resampled coord txt file>")
    print(color.GREEN + color.BOLD + "Example of usage: " + color.END)
    print(
        "python3 split_segments.py <*resampledZ.txt>")

    print()
    exit(-1)
n

for txtfile in txtfiles:
    print("Processing " + txtfile + " >>>>>>>>>>>")
    X = []
    Y = []
    A = []
    Z = []
    outputname = txtfile.replace(".txt", "_renumber.txt")
    with open(txtfile, "r") as f:
        for line in f.readlines():
            newline = line.split()
            X.append(float(newline[0]))
            Y.append(float(newline[1]))
            A.append(float(newline[2]))
            Z.append(int(newline[3]))
    total_particles = len(X)
    if total_particles == 0:
        continue

    cnt = 0
    cur_curve = Z[0]
    new_Z = [0 for i in range(total_particles)]
    curve = Z[0]
    for i in range(total_particles):
        if Z[i] == cur_curve:
            if cnt < segment_num:
                cnt = cnt + 1
                new_Z[i] = curve
            else:
                cnt = 0
                curve = curve + 1
                new_Z[i] = curve

        else:
            cnt = 0
            cur_curve = Z[i]
            curve = curve + 1
            new_Z[i] = curve
    with open(outputname, "w") as f:
        for i in range(total_particles):
            f.write(str(X[i]) + " " + str(Y[i]) + " " +
                    str(A[i]) + " " + str(new_Z[i]) + "\n")

print("Done!")
