#!/usr/bin/python3
import sys
import os
import math
import numpy as np


def distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)


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


class Star_Data():
    def __init__(self, file_path):
        self.file_path = file_path
        self.star_dict = {}
        self.particles_number = 0

    def get_data(self):
        star_dict = {}
        flag = 1
        with open(self.file_path, 'r') as f:
            cnt = 0
            for line in f.readlines():
                if line and line[0] == '_':
                    flag = 0
                    newline = line.split()
                    star_dict[newline[0][1:]] = []
                elif line and flag == 0:
                    i = 0
                    newline = line.split()
                    if len(newline) == len(star_dict):
                        for key in star_dict:
                            star_dict[key].append(newline[i])
                            i = i+1
                        cnt += 1
        self.star_dict = star_dict
        self.particles_number = cnt


def euler_angles2matrix(alpha, beta, gamma):
    matrix = np.arange(9, dtype=float)

    matrix.shape = (3, 3)
    alpha = math.radians(alpha)
    beta = math.radians(beta)
    gamma = math.radians(gamma)

    ca = math.cos(alpha)
    cb = math.cos(beta)
    cg = math.cos(gamma)
    sa = math.sin(alpha)
    sb = math.sin(beta)
    sg = math.sin(gamma)
    cc = cb * ca
    cs = cb * sa
    sc = sb * ca
    ss = sb * sa
    matrix[0, 0] = cg * cc - sg * sa
    matrix[0, 1] = cg * cs + sg * ca
    matrix[0, 2] = -cg * sb
    matrix[1, 0] = -sg * cc - cg * sa
    matrix[1, 1] = -sg * cs + cg * ca
    matrix[1, 2] = sg * sb
    matrix[2, 0] = sc
    matrix[2, 1] = ss
    matrix[2, 2] = cb
    return matrix


def print_help_message():
    print(color.RED + color.BOLD + "About this program: " + color.END)
    print("This program/script performs paticle coordinates extention/recentering to multiple positions and filtering from 2D classification or 3D reconstruction results.")
    print("This is designed for filaments objects")
    print("Supported file formats: relion star file format(end with .star)\n")
    print(color.RED + color.BOLD + "Some notes: " + color.END)
    print("Star file must be splitted first.(Each star file corresponds to one micrograph) ")
    print("Star file must include rlnCoordinateX rlnCoordinateY rlnAnglePsi")
    print("rlnAngleRot rlnAngleTilt are optional if the star file is from 2D classification results. In this case, rlnAngleRot and rlnAngleTilt are set to zero.")
    print("The output star file will only contain rlnCoordinateX rlnCoordinateY information.")

    print(color.RED + color.BOLD + "\nUsage: " + color.END)
    print("python3 " + sys.argv[0] + " [options] <coordinates_files>\n")
    print(color.RED + color.BOLD +
          "Options (many default values are used for microtubules, you should change them according to your data)" + color.END)
    print('{:30s} {:40s}'.format("arguments", "defulat values") +
          "decription")
    print('{:30s} {:40s}'.format("--image_size_x", "1024") +
          "Size of micrograph, in pixel.")
    print('{:30s} {:40s}'.format("--image_size_y", "1024") +
          "Size of micrograph, in pixel.")
    print('{:30s} {:40s}'.format("--box_size", "128") +
          "Box size of particle, in pixel. Used to remove particles near the edge.")

    print('{:30s} {:40s}'.format("--new_centers", "0 0 30 0 0 -30 0 0 60 0 0 -60") +
          "New centers, in pixel. A list of numbers.")
    print('{:30s} {:40s}'.format("", "") +
          "The coordinates for image/map center is 0 0 0")

    print('{:30s} {:40s}'.format("--filter_dis", "20") +
          "Filter distance, in pixel. Used to remove duplicated particles.")

    print('{:30s} {:40s}'.format("--merge", "1") +
          "After extension, whether or not to include the original particles. 1 for true. 0 for false")

    print(color.RED + color.BOLD + "\nExample of usage: " + color.END)
    print("python3 " +
          sys.argv[0] + " --image_size_x 1024 --image_size_y 1024 --box_size 128 --new_centers 0 0 30 0 0 -30 0 0 60 0 0 -60 --filter_dis 20 slot*.star")
    print("python3 " +
          sys.argv[0] + " --new_centers 0 30 0 0 -30 0 --filter_dis 20 slot*.star")
    print()

    print()
    exit(-1)


if len(sys.argv[:]) < 2 or "-h" in sys.argv[:] or "--h" in sys.argv[:] or "--help" in sys.argv[:] or "-help" in sys.argv[:]:
    print_help_message()

# command line processing #
arguments = {}
arguments["image_size_x"] = "1024"
arguments["image_size_y"] = "1024"
arguments["box_size"] = "128"
arguments["new_centers"] = [0, 0, 30, 0, 0, -30, 0, 0, 60, 0, 0, -60]
arguments["filter_dis"] = "20"
arguments["merge"] = "1"
arguments["files"] = []

error_flag = 0
flag = 0
for index in range(1, len(sys.argv[:])):
    item = sys.argv[index]
    if "--new_centers" in item:
        flag = 1
        arguments["new_centers"] = []
        continue
    elif "--" in item:
        flag = 0
        argument = item.replace("--", "")
        if argument in arguments.keys():
            try:
                arguments[argument] = sys.argv[index+1]
            except IndexError:
                print("ERROR: No value for " + item + "!")
                exit(-1)
        else:
            error_flag = 1
            print("ERROR: " + item + " Not in the options!")
    elif ".star" in item:
        flag = 0
        arguments["files"].append(item)
    elif flag == 1:
        arguments["new_centers"].append(float(item))

if error_flag == 1:
    exit(-1)

# arguments check #
extensions = arguments["new_centers"]
if len(arguments["new_centers"]) % 3 != 0:
    print()
    print("ERROR! Please provide coordinates of multiples of three.\n")
    exit(-1)

print(color.RED + color.BOLD + "Using the following parameters: " + color.END)
for key, item in arguments.items():
    if key != "files" and key != "new_centers":
        print('{:30s} {:20s}'.format("--"+key, item))
    elif key == "new_centers":
        print("--new_centers ")
        for index in range(int(len(extensions)/3)):
            new_index = index*3
            print(str(extensions[new_index]) + " " +
                  str(extensions[new_index+1]) + " " + str(extensions[new_index+2]))
    else:
        print(color.RED + color.BOLD + "\nThe files are: " + color.END)
        if len(arguments["files"]) == 0:
            print("No file input!!Please make sure that files end with .star")
            exit(-1)
        for coords_file in arguments["files"]:
            print(coords_file)
print()
# input transform to program #
image_size_x = float(arguments["image_size_x"])
image_size_y = float(arguments["image_size_y"])
box_size = float(arguments["box_size"])
filter_dis = float(arguments["filter_dis"])
merge_flag = int(arguments["merge"])
centers = {}
for i in range(int(len(extensions)/3)):
    index = 3*i
    centers[i] = extensions[index:index+3]


# processing #
for star_file in arguments["files"][:]:

    # check files
    if os.path.exists(star_file) != True:
        print("No such file: " + star_file)
        continue
    if merge_flag == 1:
        outputfilename = star_file.replace(
            ".star", "_extend_merge_filter.star")
    else:
        outputfilename = star_file.replace(".star", "_extend_filter.star")
    output = open(outputfilename, "w")
    output.write(
        "\ndata_images\n\nloop_\n_rlnCoordinateX #1\n_rlnCoordinateY #2\n")
    print("Wrote " + outputfilename)

    # prepare data
    data = Star_Data(star_file)
    data.get_data()
    X = [float(item) for item in data.star_dict["rlnCoordinateX"]]
    Y = [float(item) for item in data.star_dict["rlnCoordinateY"]]
    Psi = [float(item) for item in data.star_dict["rlnAnglePsi"]]
    if "rlnAngleRot" in data.star_dict.keys():
        Rot = [float(item) for item in data.star_dict["rlnAngleRot"]]
    else:
        Rot = [0 for item in data.star_dict["rlnAnglePsi"]]

    if "rlnAngleTilt" in data.star_dict.keys():
        Tilt = [float(item) for item in data.star_dict["rlnAngleTilt"]]
    else:
        Tilt = [0 for item in data.star_dict["rlnAnglePsi"]]

    # extend center, remove edge particles
    all_x = []
    all_y = []
    for i in range(data.particles_number):
        if X[i] > box_size/2 and Y[i] > box_size/2 and X[i] < (image_size_x - box_size/2) and Y[i] < (image_size_y - box_size/2) and merge_flag == 1:
            all_x.append(float(X[i]))
            all_y.append(float(Y[i]))
        for key in centers.keys():
            recenter = np.arange(3)
            recenter[0] = centers[key][0]
            recenter[1] = centers[key][1]
            recenter[2] = centers[key][2]
            euler_matrix = euler_angles2matrix(Rot[i], Tilt[i], Psi[i])

            projected_center = np.matmul(euler_matrix, recenter)
            new_x = X[i] - projected_center[0]
            new_y = Y[i] - projected_center[1]
            if new_x > box_size/2 and new_y > box_size/2 and new_x < (image_size_x - box_size/2) and new_y < (image_size_y - box_size/2):
                all_x.append(float(new_x))
                all_y.append(float(new_y))

    # filtering
    count = len(all_x)
    all_z = [0 for item in range(count)]
    collected = [1 for item in range(count)]
    for i in range(count):
        for j in range(i+1, count, 1):
            dis = distance(all_x[i], all_y[i], all_z[i],
                           all_x[j], all_y[j], all_z[j])
            if dis < filter_dis:
                collected[i] = 0
                break
    for i in range(count):
        if collected[i] == 1:
            output.write(str(all_x[i]) + " " + str(all_y[i]) + "\n")

    output.close()
print("Finished!")
print(color.BOLD + "<<<<<  A Kind Reminding: if you find this script useful, please acknowledge Pengxin Chai from Dr. Kai Zhang lab at Yale MB&B.  >>>>>" + color.END)
