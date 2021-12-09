import sys
import math

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

                    if len(newline) > 0:
                        for key in star_dict:
                            star_dict[key].append(newline[i])
                            i = i+1
                        cnt += 1
        self.star_dict = star_dict
        self.particles_number = cnt

    def print_head(self):
        keys = ""
        for key in self.star_dict.keys():
            keys += key
            keys += " "
        if keys:
            print(keys)
        else:
            print("Warning".upper() +
                  ": No head in this star object: " + self.file_path)

    def print_lines(self, num=5):
        self.print_head()
        for i in range(num):
            try:
                line = ""
                for key, value in self.star_dict.items():
                    line += str(value[i])
                    line += " "
                if line:
                    print(line)
            except IndexError:
                break

if len(sys.argv[:])<4:
    print("Usage: python3 " + sys.argv[0] + " <star file> <reference star file> <distance pixel>")
    print("This program is used to filter the particles' coordinates based on reference coordinates.")
    exit(-1)
star_file = sys.argv[1]
reference_file = sys.argv[2]
min_distance_pixel = float(sys.argv[3])

star_file_data = Star_Data(star_file)
reference_file_data = Star_Data(reference_file)

star_file_data.get_data()
reference_file_data.get_data()

x = [float(item) for item in star_file_data.star_dict["rlnCoordinateX"]]
y = [float(item) for item in star_file_data.star_dict["rlnCoordinateY"]]
x_ref = [float(item)
         for item in reference_file_data.star_dict["rlnCoordinateX"]]
y_ref = [float(item)
         for item in reference_file_data.star_dict["rlnCoordinateY"]]
collected = [0 for i in range(star_file_data.particles_number)]

for i in range(star_file_data.particles_number):
    flag = 1
    for j in range(reference_file_data.particles_number):
        distance_pixel = math.sqrt((x[i]-x_ref[j])**2 + (y[i]-y_ref[j])**2)
        if distance_pixel < min_distance_pixel:
            flag = 0
            break

    if flag == 1:
        collected[i] = 1


output_filename = star_file.replace(".star", "_filter.star")
output = open(output_filename, "w")
output.write("\ndata_\n\nloop_\n")
for index, key in enumerate(star_file_data.star_dict.keys()):
    output.write("_" + key)
    output.write(" #" + str(index))
    output.write("\n")

for i in range(star_file_data.particles_number):
    if collected[i] == 0:
        for key, value in star_file_data.star_dict.items():
            output.write(str(value[i]))
            output.write(" ")
        output.write("\n")
output.close()
