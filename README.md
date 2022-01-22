# multi-curve fitting
This folder contains the python scripts to perform multi-curves fitting and other scripts for relion starfile processing. 

The scripts were written using Python language (python3). It only uses some standard packages and should be easily running. 
Type the following command to see the help message:

**python3 mcurve_fitting_2D.py --help**
You should see the message like below: 
**About this program: **
This program/script performs multi-curves fitting of the input coordinates (2D).
Supported file formats: relion star file format(end with .star) or 2-column txt file format(end with .txt)
**
Some notes:** 
Star file must include rlnCoordinateX rlnCoordinateY
The output files contain the cluster results of original coordinates(_Zscore),resampled coordinates(_resam_Zscore) both in star and txt file format.
The program uses polynomial fitting. If you don't like this estimation but are satisfied with the cluster results, you can use other fitting methods for each curve.
The resampled file has two additional columns: rlnAnglePsi and rlnParticleSelectZScore;  rlnAnglePsi is the angle between tangent and X axis, rlnParticleSelectZScore is the curve number.
The speed of program is generaly fast. It takes about 10mins to finish 3k star files.(using default intergration_step_ang)


**Usage:** 
python3 mcurve_fitting_2D.py [options] <coordinates_files>

Options (many default values are used for microtubules, you should change them according to your data)
arguments                      defulat values      decription
--pixel_size_ang               1.33                Pixel size of the micrograph/coordinate, in angstrom.
--sample_step_ang              41                  Final sampling step, usually the length of repeating unit. 41 is the length of tubulin subunit, in angstrom
--intergration_step_ang        1                   Intergration step during curve length calculation(resampling). in angstrom. 1~5 is generaly good. The bigger the faster, but less accurate.
--poly_expon                   3                   The polynomial factor during the curve growth and final resampling steps.

**Example of usage: **
python3 mcurve_fitting_2D.py --pixel_size_ang 1.33 --sample_step_ang 41 --poly_expon 3 Falcon*.star
python3 mcurve_fitting_2D.py --pixel_size_ang 1 --sample_step_ang 41 --poly_expon 2 --min_number_growth 2 --max_seed_fitting_error 2 Falcon*.txt



More documentation soon.
