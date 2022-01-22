# multi-curve fitting
This folder contains the python scripts to perform multi-curves fitting and other scripts for relion starfile processing. 

The scripts were written using Python language (python3). It only uses some standard packages and should be easily running. 
Type the following command to see the help message:

**python3 mcurve_fitting_2D.py --help**

You should see the message like below: 

About this program: 

This program/script performs multi-curves fitting of the input coordinates (2D).

Supported file formats: relion star file format(end with .star) or 2-column txt file format(end with .txt)

Usage: 

python3 mcurve_fitting_2D.py [options] <coordinates_files>

Example of usage:

python3 mcurve_fitting_2D.py --pixel_size_ang 1.33 --sample_step_ang 41 --poly_expon 3 Falcon*.star


***********************************
The difference between mcurve_fitting_2D.py and mcurve_fitting_2D_for_helical.py is the output format. The mcurve_fitting_2D_for_helical.py outputs the star file which matches the Relion helical auto-picking format. That being said, if you want to perform helical reconstruction, you can use this script.  





**********************************
More documentation soon.
