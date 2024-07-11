#Download

git clone https://github.com/PengxinChai/multi-curve-fitting

git clone https://github.com/PengxinChai/tubulin-lattice-subtraction

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
This manual is for MT-signal subtraction under cryoSPARC processing pipeline:

Preprocessing 
Run cryoSPARC or cryoSPARC Live or Relion ro preprocess your data as usual
Pick MT particles as many as possible (8nm cutoff using template matching) and run two-three iterative 2D classification jobs to filter out junk particles. Make sure the MT is properly picked.
Use MT templates
Picking parametes: 
diameter set to 320Å
distance ratio set to 0.25 (picked 8nm particles)
extraction particles box size 512, downsample to 128 (bin4)
Select MT 2D classes 

Convert cryoSPARC file to RELION 3.0 Star format
Navigate to the “2D classes selection job” in JXX and run the following command:

“csparc2star.py --swapxy particles_selected.cs JXX_passthrough_particles_selected.cs particles_selected.star”

This will create the “particles_selected.star” which will be used for multi-curve fitting. 

Navigate to the cryosparc session folder, for example, in “/PX/SX”

Make two folders called “ori_mics” and “sub_mics”
“mkdir ori_mics sub_mics”

Move the micrographs from motioncorrecded folder into “ori_mics”:
“mv motioncorredted/*doseweighted.mrc ori_mics”

Navigate into “ori_mics” folder:
“cd ori_mics”

Copy the “particles_selected.star” in this folder.
“cp ../../JXX/particles_oriselected.star .”

Recenter the “particles_selected.star”” file:

“star_origin0_scale.com 4 particles_selected.star”

“4” is the scaling factor. This depends on the particle's extraction. If the box size is 512 and binned to 128, then the factor is “4”. If the box size is 512 and binned to 256, then the factor is “2”.

Split the  “particles_selected_origin0.star” into into individual files using the following command:

“star_split_quick.py particles_selected_origin0.star *doseweighted.mrc”

 Perform multi-curve fitting
In the motion-corrected folder,  run the following command:

“mcurve_fitting_2D.py -h”
“mcurve_fitting_2D.py --pixel_size_ang 0.868 --poly_expon 2 XXX_split.star”

Split each MT segment into smaller segments. It has been found that the subtraction is more clean when subtracting smaller segments for MT singlets. For MT doublet, this step is not necessary. It is because MT singlet is more heterogeneous(non-uniform diameter, helical twist) than MT doublet. 

“split_segments.py XXX_split_resam_Zscore.txt”

This will generate small segments and each one has ~20 coordinates (~80nm/segment). The file end with “split_resam_Zscore_renumber.txt”

Prepare mask for MT signal subtraction
Copy the  mask into the folder:

“cp common_masks/XXX.mrc .”

Large scale  MT signal subtraction
Copy subtraction script into the folder:

“cp mrc_2d_curve_weaken_one.sh .”

Edit the script using Vim or gedit to change the files names 

Test the subtraction:
“./mrc_2d_curve_weaken_one.sh XXX_doseweighted.mrc”


Para run the subtraction:
“para_run.py   32   ./mrc_2d_curve_weaken_one.sh    XXX*_doseweighted.mrc”

Move subtracted micrographs into “sub_mics” folder
Navigate to the session folder
move the subtracted micrographs into sub_mics:
“mv ori_mics/*sub.mrc sub_mics”

Change the name of subtracted micrographs:
“rename sub.mrc .mrc sub_mics/*sub.mrc”


Link subtracted micrographs into motioncorrected micrographs:
           “cd motioncorrected”
“ln -s ../sub_mics/*doseweighted.mrc .”
“ln -s ../ori_mics/*doseweighted.mrc .”
(because some micrographs don’t have MT for subtraction, we need to link these original micrographs for cryoSparc to run. )

