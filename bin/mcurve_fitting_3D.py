#!/usr/bin/python3
import sys
import os
import math
import numpy as np


# functions and class
def distance_two_points(x1, y1, k1, x2, y2, k2):
    dist = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (k2-k1)**2)
    return dist


def find_seed(i, j, X, Y, K, Z):
    tmp_Z = [i, j]
    number = 2

    a = Y[i] - Y[j]
    b = X[j] - X[i]
    c = X[i]*Y[j] - X[j]*Y[i]
    delta_z = abs(K[i] - K[j])
    if delta_z > max_distance_to_line:
        return tmp_Z

    z_ave = (K[i] + K[j])/2
    while True:
        flag = 0
        for k in range(0, total_number, 1):
            if Z[k] != -1:
                continue
            if Z[i] != -1 or Z[j] != -1:
                flag = 0
                break
            if k in tmp_Z:
                continue

            dis_to_line = (a*X[k] + b*Y[k] + c) / math.sqrt(a*a+b*b)
            delta_z = abs(K[k] - z_ave)

            if abs(dis_to_line) < max_distance_to_line and delta_z < max_distance_to_line:
                min_dis = 100000
                for index in tmp_Z:
                    dis_index_k = distance_two_points(
                        X[index], Y[index], 0, X[k], Y[k], 0)
                    if dis_index_k < min_dis:
                        min_dis = dis_index_k

                if min_dis > min_distance_in_extension_seed and min_dis < max_distance_in_extension_seed:
                    tmp_Z.append(k)
                    number += 1
                    flag = 1
                    if number < min_number:
                        break
                    else:
                        flag = 0
                        break

        if flag == 0:
            break
    return tmp_Z


def angle_evaluate(poly, point, mode):
    evaluation_step = 40/pixel_size_ang
    result = 1
    if mode == 1:
        accumulation = 0
        current_x = point
        current_y = poly(current_x)
        next_x = current_x + intergration_step
        next_y = poly(next_x)
        slope_one = (next_y-current_y)/(next_x-current_x)
        angle_one = math.degrees(math.atan(slope_one))
        while accumulation < evaluation_step:
            next_x = current_x + intergration_step
            next_y = poly(next_x)
            dist = distance_two_points(
                current_x, current_y, 0, next_x, next_y, 0)
            accumulation += dist
            current_x = next_x
            current_y = next_y
        next_x = current_x + intergration_step
        next_y = poly(next_x)
        slope_two = (next_y-current_y)/(next_x-current_x)
        angle_two = math.degrees(math.atan(slope_two))
        angle_change = abs(angle_two-angle_one)
    else:
        accumulation = 0
        current_y = point
        current_x = poly(current_y)
        next_y = current_y + intergration_step
        next_x = poly(next_y)
        if (abs(next_x-current_x)) > 0.0001:
            slope_one = (next_y-current_y)/(next_x-current_x)
            angle_one = math.degrees(math.atan(slope_one))
        else:
            angle_one = 90
        while accumulation < evaluation_step:
            next_y = current_y + intergration_step
            next_x = poly(next_y)
            dist = distance_two_points(
                current_x, current_y, 0, next_x, next_y, 0)
            accumulation += dist
            current_x = next_x
            current_y = next_y
        next_y = current_y + intergration_step
        next_x = poly(next_y)
        if (abs(next_x - current_x)) > 0.0001:
            slope_two = (next_y-current_y)/(next_x-current_x)
            angle_two = math.degrees(math.atan(slope_two))
        else:
            angle_two = 90
        angle_change = abs(angle_two-angle_one)
    if angle_change >= max_angle_change_per_4nm:
        result = 0
    else:
        result = 1
    return result


def resample(poly, polyk, left, right, mode, sample_step, cluster):

    if mode == 1:  # y=f(x) k = f(x)
        accumulation = 0
        current_x = left
        current_y = poly(current_x)
        current_k = polyk(current_x)
        while current_x < right:
            next_x = current_x + intergration_step
            next_y = poly(next_x)
            next_k = polyk(next_x)
            dist = distance_two_points(
                current_x, current_y, current_k, next_x, next_y, next_k)
            accumulation += dist
            if sample_step <= accumulation:
                accumulation = 0
                slope = (next_y - current_y)/(next_x - current_x)
                angle = math.degrees(math.atan(slope))
                d = math.sqrt((next_x-current_x)**2 + (next_y-current_y)**2)
                slopek = (next_k - current_k)/d
                anglek = math.degrees(math.atan(slopek))
                output_resam_Zscore.write(str(current_x) + " ")
                output_resam_Zscore.write(str(current_y) + " ")
                output_resam_Zscore.write(str(current_k) + " ")
                output_resam_Zscore.write(str(angle) + " ")
                output_resam_Zscore.write(str(anglek) + " ")
                output_resam_Zscore.write(str(cluster) + "\n")

                output_resam_Zscore_txt.write(str(current_x) + " ")
                output_resam_Zscore_txt.write(str(current_y) + " ")
                output_resam_Zscore_txt.write(str(current_k) + " ")
                output_resam_Zscore_txt.write(str(angle) + " ")
                output_resam_Zscore_txt.write(str(anglek) + " ")
                output_resam_Zscore_txt.write(str(cluster) + "\n")
            current_x = next_x
            current_y = next_y
            current_k = next_k
    else:  # x = f(y) k = f(y)
        accumulation = 0
        current_y = left
        current_x = poly(current_y)
        current_k = polyk(current_y)
        while current_y < right:
            next_y = current_y + intergration_step
            next_x = poly(next_y)
            next_k = polyk(next_y)
            dist = distance_two_points(
                current_x, current_y, current_k, next_x, next_y, next_k)
            accumulation += dist
            if sample_step <= accumulation:
                accumulation = 0
                slope = (next_x - current_x)/(next_y - current_y)
                angle = 90-math.degrees(math.atan(slope))
                d = math.sqrt((next_x-current_x)**2 + (next_y-current_y)**2)
                slopek = (next_k - current_k)/d
                anglek = math.degrees(math.atan(slopek))
                output_resam_Zscore.write(str(current_x) + " ")
                output_resam_Zscore.write(str(current_y) + " ")
                output_resam_Zscore.write(str(current_k) + " ")
                output_resam_Zscore.write(str(angle) + " ")
                output_resam_Zscore.write(str(anglek) + " ")
                output_resam_Zscore.write(str(cluster) + "\n")

                output_resam_Zscore_txt.write(str(current_x) + " ")
                output_resam_Zscore_txt.write(str(current_y) + " ")
                output_resam_Zscore_txt.write(str(current_k) + " ")
                output_resam_Zscore_txt.write(str(angle) + " ")
                output_resam_Zscore_txt.write(str(anglek) + " ")
                output_resam_Zscore_txt.write(str(cluster) + "\n")

            current_x = next_x
            current_y = next_y
            current_k = next_k


def seed_extension(tmp_Z, X, Y, Z, cluster):
    seed_evaluation = 1
    seed_angle_evalution = 1
    X_cluster = []
    Y_cluster = []
    K_cluster = []
    for index in tmp_Z:
        X_cluster.append(X[index])
        Y_cluster.append(Y[index])
        K_cluster.append(K[index])
        Z[index] = cluster
    delta_x = abs(max(X_cluster) - min(X_cluster))
    delta_y = abs(max(Y_cluster) - min(Y_cluster))

    if delta_x >= delta_y:
        coeff = np.polyfit(X_cluster, Y_cluster, poly_expon)
        poly = np.poly1d(coeff)
        coeff_seed = np.polyfit(X_cluster, Y_cluster, poly_expon_seed)
        poly_seed = np.poly1d(coeff_seed)

        coeffk = np.polyfit(X_cluster, K_cluster, poly_expon)
        polyk = np.poly1d(coeffk)
        for index in tmp_Z:
            if abs(poly_seed(X[index]) - Y[index]) >= seed_evaluation_constant:
                seed_evaluation = 0
        seed_angle_evalution = angle_evaluate(
            poly, (min(X_cluster)+max(X_cluster))/2, 1)
        while True:
            flag = 0
            for k in range(0, total_number, 1):
                if Z[k] != -1:
                    continue
                if k in tmp_Z:
                    continue
                dis_to_curve = abs(poly(X[k]) - Y[k])
                dis_to_curve_z = abs(polyk(X[k]) - K[k])
                if dis_to_curve < max_distance_to_curve and dis_to_curve_z < max_distance_to_curve:
                    min_dis = 100000
                    for index in tmp_Z:
                        dis_index_k = distance_two_points(
                            X[index], Y[index], 0, X[k], Y[k], 0)
                        if dis_index_k < min_dis:
                            min_dis = dis_index_k
                    if min_dis > min_distance_in_extension and min_dis < max_distance_in_extension:
                        flag = 1
                        Z[k] = cluster
                        tmp_Z.append(k)
                        X_cluster.append(X[k])
                        Y_cluster.append(Y[k])
                        K_cluster.append(K[k])
                        coeff = np.polyfit(X_cluster, Y_cluster, poly_expon)
                        poly = np.poly1d(coeff)
                        coeffk = np.polyfit(X_cluster, K_cluster, poly_expon)
                        polyk = np.poly1d(coeffk)

            if flag == 0:
                break
        mode = 1
    else:
        coeff = np.polyfit(Y_cluster, X_cluster, poly_expon)
        poly = np.poly1d(coeff)

        coeff_seed = np.polyfit(Y_cluster, X_cluster, poly_expon_seed)
        poly_seed = np.poly1d(coeff_seed)

        coeffk = np.polyfit(Y_cluster, K_cluster, poly_expon)
        polyk = np.poly1d(coeffk)
        for index in tmp_Z:
            if abs(poly_seed(Y[index]) - X[index]) >= seed_evaluation_constant:
                seed_evaluation = 0
        seed_angle_evalution = angle_evaluate(
            poly, (min(Y_cluster)+max(Y_cluster))/2, 0)
        while True:
            flag = 0
            for k in range(0, total_number, 1):
                if Z[k] != -1:
                    continue
                if k in tmp_Z:
                    continue
                dis_to_curve = abs(poly(Y[k]) - X[k])
                dis_to_curve_z = abs(polyk(Y[k]) - K[k])

                if dis_to_curve < max_distance_to_curve and dis_to_curve_z < max_distance_to_curve:
                    min_dis = 100000
                    for index in tmp_Z:
                        dis_index_k = distance_two_points(
                            X[index], Y[index], 0, X[k], Y[k], 0)
                        if dis_index_k < min_dis:
                            min_dis = dis_index_k
                    if min_dis > min_distance_in_extension and min_dis < max_distance_in_extension:
                        flag = 1
                        Z[k] = cluster
                        tmp_Z.append(k)
                        X_cluster.append(X[k])
                        Y_cluster.append(Y[k])
                        K_cluster.append(K[k])
                        coeff = np.polyfit(Y_cluster, X_cluster, poly_expon)
                        poly = np.poly1d(coeff)
                        coeffk = np.polyfit(Y_cluster, K_cluster, poly_expon)
                        polyk = np.poly1d(coeffk)
            if flag == 0:
                break
        mode = 0

    if (len(tmp_Z) - min_number) >= extension_min_number and seed_evaluation == 1 and seed_angle_evalution == 1:
        print("Seed searching, evaluation and growth successfully! Start to resample: ")
        #print(X_cluster, Y_cluster, K_cluster)
        for index in tmp_Z:
            output_Zscore.write(str(X[index]) + " ")
            output_Zscore.write(str(Y[index]) + " ")
            output_Zscore.write(str(K[index]) + " ")
            output_Zscore.write(str(cluster))
            output_Zscore.write("\n")
            output_Zscore_txt.write(str(X[index]) + " ")
            output_Zscore_txt.write(str(Y[index]) + " ")
            output_Zscore_txt.write(str(K[index]) + " ")
            output_Zscore_txt.write(str(cluster))
            output_Zscore_txt.write("\n")

        if mode == 1:
            resample(poly, polyk, min(X_cluster), max(
                X_cluster), 1, sample_step, cluster)
        else:
            resample(poly, polyk, min(Y_cluster), max(
                Y_cluster), 0, sample_step, cluster)
        print("Done resampling! " + "cluster " + str(cluster) + "\n")
        return 1
    else:
        for index in tmp_Z:
            Z[index] = -1
        return 0


# star class #
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
# end of function and class #


def print_help_message():
    print(color.RED + color.BOLD + "About this program: " + color.END)
    print("This program/script performs multi-curves fitting of the input coordinates (3D).")
    print("Supported file formats: relion star file format(end with .star) or 3-column txt file format(end with .txt)\n")
    print(color.RED + color.BOLD + "Some notes: " + color.END)
    print("Star file must include rlnCoordinateX rlnCoordinateY rlnCoordinateZ")
    print("The output files contain the cluster results of original coordinates(_Zscore),resampled coordinates(_resam_Zscore) both in star and txt file format.")
    print("The program uses polynomial fitting. If you don't like this estimation but are satisfied with the cluster results, you can use other fitting methods for each curve.")
    print("The resampled file has 3 additional columns: rlnAngleYX rlnAngleZXY and rlnParticleSelectZScore")
    print("For 3D curve projected in XY plane, rlnAngleYX is the angle between 2D curve's tangent and X axis")
    print("rlnAngleZXY is the angle between tangent and XY plane")
    print("The speed of program is generaly fast. It takes about 10mins to finish 3k star files.(using default intergration_step_ang)\n")

    print(color.RED + color.BOLD + "\nUsage: " + color.END)
    print("python3 " + sys.argv[0] + " [options] <coordinates_files>\n")
    print(color.RED + color.BOLD +
          "Options (many default values are used for microtubules, you should change them according to your data)" + color.END)
    print('{:30s} {:20s}'.format("arguments", "defulat values") +
          "decription")
    print('{:30s} {:20s}'.format("--pixel_size_ang", "5.33") +
          "Pixel size of the micrograph/coordinate, in angstrom.")
    print('{:30s} {:20s}'.format("--sample_step_ang", "41") +
          "Final sampling step, usually the length of repeating unit. 41 is the length of tubulin subunit, in angstrom")
    print('{:30s} {:20s}'.format("--intergration_step_ang", "1") +
          "Intergration step during curve length calculation(resampling). in angstrom. 1~5 is generaly good. The bigger the faster, but less accurate.")
    print('{:30s} {:20s}'.format("--poly_expon", "3") +
          "The polynomial factor during the curve growth and final resampling steps.")

    print('{:30s} {:20s}'.format(
        "\nOptions for seed searching and evaluation", ""))
    print('{:30s} {:20s}'.format("--min_number_seed", "5") +
          "Minimal number of points to form the seed. 5 to 7 are reasonable.")
    print('{:30s} {:20s}'.format("--max_dis_to_line_ang", "50") +
          "The seed searching starts with a line from two adjacent points.")
    print('{:30s} {:20s}'.format("", "") +
          "If the next point is close to this line (and meets the next two requirements), the point is added. in angstrom.")
    print('{:30s} {:20s}'.format("--min_dis_neighbor_seed_ang", "60") +
          "The mininal distance between neighbor points, in angstrom.")
    print('{:30s} {:20s}'.format("--max_dis_neighbor_seed_ang", "320") +
          "The maximal distance between neighbor points, in angstrom.")
    print('{:30s} {:20s}'.format("--poly_expon_seed", "2") +
          "The polymomial factor for seed evaluation (see the following two parameters). 2 or 3 is good. Not recommended to use bigger values.")
    print('{:30s} {:20s}'.format("--max_seed_fitting_error", "1") +
          "When the initial seed is found,the program fits an intial function. The maximal error for the fitting. 1~5 are good. ")
    print('{:30s} {:20s}'.format("", "") +
          "If the points are well-centered, use smaller value.")
    print('{:30s} {:20s}'.format("--max_angle_change_per_4nm", "0.5") +
          "The curvature restriction. For microtubules, the angle change/4nm is very small. Use bigger value to disable this option, in degree.")

    print('{:30s} {:20s}'.format(
        "\nOptions for seed growth and evaluation", ""))
    print('{:30s} {:20s}'.format("--max_dis_to_curve_ang", "40") +
          "If the point is close to this curve (and meets the next two requirements), the point is added and the function is updated. in angstrom.")
    print('{:30s} {:20s}'.format("--min_dis_neighbor_curve_ang", "60") +
          "The minimal distance between neighbor points, usually the same as seed parameters. in angstrom.")
    print('{:30s} {:20s}'.format("--max_dis_neighbor_curve_ang", "320") +
          "The maximal distance between neighbor points, usually the same as seed parameters. in angstrom.")
    print('{:30s} {:20s}'.format("--min_number_growth", "0") +
          "The minimal number of points added. This number plus min_number_seed together define the minimal number of the curve.")

    print(color.RED + color.BOLD + "\nExample of usage: " + color.END)
    print("python3 " +
          sys.argv[0] + " --pixel_size_ang 1.33 --sample_step_ang 41 --poly_expon 3 Falcon*.star")
    print("python3 " +
          sys.argv[0] + " --pixel_size_ang 1 --sample_step_ang 41 --poly_expon 2 --min_number_growth 2 --max_seed_fitting_error 2 Falcon*.txt\n")
    print()
    exit(-1)


if len(sys.argv[:]) < 2 or "-h" in sys.argv[:] or "--h" in sys.argv[:] or "--help" in sys.argv[:] or "-help" in sys.argv[:]:
    print_help_message()


# command line processing #
arguments = {}
arguments["pixel_size_ang"] = "5.33"
arguments["sample_step_ang"] = "41"
arguments["intergration_step_ang"] = "1"
arguments["poly_expon"] = "3"
arguments["min_number_seed"] = "5"
arguments["max_dis_to_line_ang"] = "50"
arguments["min_dis_neighbor_seed_ang"] = "60"
arguments["max_dis_neighbor_seed_ang"] = "320"
arguments["poly_expon_seed"] = "2"
arguments["max_seed_fitting_error"] = "1"
arguments["max_angle_change_per_4nm"] = "0.5"
arguments["max_dis_to_curve_ang"] = "40"
arguments["min_dis_neighbor_curve_ang"] = "60"
arguments["max_dis_neighbor_curve_ang"] = "320"
arguments["min_number_growth"] = "0"
arguments["files"] = []
error_flag = 0

for index in range(1, len(sys.argv[:])):
    item = sys.argv[index]
    if "--" in item:
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
    elif ".star" in item or ".txt" in item:
        arguments["files"].append(item)

if error_flag == 1:
    exit(-1)


print(color.RED + color.BOLD + "Using the following parameters: " + color.END)
for key, item in arguments.items():
    if key != "files":
        print('{:30s} {:20s}'.format("--"+key, item))
    else:
        print(color.RED + color.BOLD + "\nThe files are: " + color.END)
        if len(arguments["files"]) == 0:
            print("No file input!!Please make sure that files end with .star or .txt")
            exit(-1)
        for coords_file in arguments["files"]:
            print(coords_file)
print(color.RED + color.BOLD + "\nStart processing: " + color.END)

# parameters in program #
file_paths = arguments["files"]
pixel_size_ang = float(arguments["pixel_size_ang"])
poly_expon = int(arguments["poly_expon"])
ang_sample_step = float(arguments["sample_step_ang"])
intergration_step_ang = float(arguments["intergration_step_ang"])

# seed searching and evalution parameters
min_number = int(arguments["min_number_seed"])
ang_max_distance_to_line = float(arguments["max_dis_to_line_ang"])
ang_min_distance_in_extension_seed = float(
    arguments["min_dis_neighbor_seed_ang"])
ang_max_distance_in_extension_seed = float(
    arguments["max_dis_neighbor_seed_ang"])
poly_expon_seed = int(arguments["poly_expon_seed"])
seed_evaluation_constant = float(arguments["max_seed_fitting_error"])
max_angle_change_per_4nm = float(arguments["max_angle_change_per_4nm"])

# growth parameters
ang_max_distance_to_curve = float(arguments["max_dis_to_curve_ang"])
ang_min_distance_in_extension = float(arguments["min_dis_neighbor_curve_ang"])
ang_max_distance_in_extension = float(arguments["max_dis_neighbor_curve_ang"])
extension_min_number = int(arguments["min_number_growth"])

# ******************** Input transformation in programs
sample_step = ang_sample_step/pixel_size_ang
intergration_step = intergration_step_ang/pixel_size_ang
max_distance_to_line = ang_max_distance_to_line/pixel_size_ang
max_distance_to_curve = ang_max_distance_to_curve/pixel_size_ang
min_distance_in_extension_seed = ang_min_distance_in_extension_seed/pixel_size_ang
max_distance_in_extension_seed = ang_max_distance_in_extension_seed/pixel_size_ang
min_distance_in_extension = ang_min_distance_in_extension/pixel_size_ang
max_distance_in_extension = ang_max_distance_in_extension/pixel_size_ang

for file_path in file_paths[:]:
    if os.path.exists(file_path) != True:
        print("No such file: " + file_path)
        continue
    print(color.RED + color.BOLD + "\nStart processing: " + file_path + color.END)
    if ".star" in file_path:
        star_file_path = file_path
        output_filename_Zscore = star_file_path.replace(
            ".star", "_Zscore.star")
        output_filename_resam_Zscore = star_file_path.replace(
            ".star", "_resam_Zscore.star")
        output_filename_Zscore_txt = star_file_path.replace(
            ".star", "_Zscore.txt")
        output_filename_resam_Zscore_txt = star_file_path.replace(
            ".star", "_resam_Zscore.txt")
        output_Zscore = open(output_filename_Zscore, "w")
        output_resam_Zscore = open(output_filename_resam_Zscore, "w")
        output_Zscore_txt = open(output_filename_Zscore_txt, "w")
        output_resam_Zscore_txt = open(output_filename_resam_Zscore_txt, "w")

        output_Zscore.write(
            "\ndata_\n\nloop_\n_rlnCoordinateX #1\n_rlnCoordinateY #2\n_rlnCoordinateZ #3\n_rlnParticleSelectZScore #4\n")
        output_resam_Zscore.write(
            "\ndata_\n\nloop_\n_rlnCoordinateX #1\n_rlnCoordinateY #2\n_rlnCoordinateZ #3\n_rlnAngleYX #4\n_rlnAngleZXY #5\n_rlnParticleSelectZScore #6\n")

        data = Star_Data(star_file_path)
        data.get_data()
        total_number = data.particles_number
        print("Number of particles: " + str(total_number))
        X = [float(value) for value in data.star_dict["rlnCoordinateX"]]
        Y = [float(value) for value in data.star_dict["rlnCoordinateY"]]
        K = [float(value) for value in data.star_dict["rlnCoordinateZ"]]
        Z = [-1 for i in range(total_number)]
    elif ".txt" in file_path:
        star_file_path = file_path.replace(".txt", ".star")
        output_filename_Zscore = star_file_path.replace(
            ".star", "_Zscore.star")
        output_filename_resam_Zscore = star_file_path.replace(
            ".star", "_resam_Zscore.star")
        output_filename_Zscore_txt = star_file_path.replace(
            ".star", "_Zscore.txt")
        output_filename_resam_Zscore_txt = star_file_path.replace(
            ".star", "_resam_Zscore.txt")
        output_Zscore = open(output_filename_Zscore, "w")
        output_resam_Zscore = open(output_filename_resam_Zscore, "w")
        output_Zscore_txt = open(output_filename_Zscore_txt, "w")
        output_resam_Zscore_txt = open(output_filename_resam_Zscore_txt, "w")
        output_Zscore.write(
            "\ndata_\n\nloop_\n_rlnCoordinateX #1\n_rlnCoordinateY #2\n_rlnCoordinateZ #3\n_rlnParticleSelectZScore #4\n")
        output_resam_Zscore.write(
            "\ndata_\n\nloop_\n_rlnCoordinateX #1\n_rlnCoordinateY #2\n_rlnCoordinateZ #3\n_rlnAngleYX #4\n_rlnAngleZXY #5\n_rlnParticleSelectZScore #6\n")
        X = []
        Y = []
        K = []
        Z = []
        with open(file_path, "r") as f:
            for line in f.readlines():
                newline = line.split()
                X.append(float(newline[0]))
                Y.append(float(newline[1]))
                K.append(float(newline[2]))
                Z.append(-1)
        total_number = len(Z)
        print("Number of particles: " + str(total_number))

        # ***************** seed and extension
    cluster = -1
    for i in range(0, total_number, 1):
        for j in range(i+1, total_number, 1):
            dis_i_j = distance_two_points(X[i], Y[i], 0, X[j], Y[j], 0)
            if dis_i_j > min_distance_in_extension_seed and dis_i_j < max_distance_in_extension_seed:

                tmp_Z = find_seed(i, j, X, Y, K, Z)
                if len(tmp_Z) == min_number:
                    cluster += 1
                    result = seed_extension(tmp_Z, X, Y, Z, cluster)
                    if result == 0:
                        cluster -= 1

    # *************** close files
    output_Zscore.close()
    output_resam_Zscore.close()
    output_Zscore_txt.close()
    output_resam_Zscore_txt.close()


print("Finished!")
print(color.BOLD + "<<<<<  A Kind Reminding: if you find this script useful, please acknowledge Pengxin Chai from Dr. Kai Zhang lab at Yale MB&B.  >>>>>" + color.END)
