# MT-Signal Subtraction Manual for cryoSPARC Users

# Formatted by chatGPT

**Kai Zhang Lab, Yale**  
**Last updated: April 2025**

This manual details how to perform microtubule (MT) signal subtraction under the **cryoSPARC** processing pipeline. You will need some command-line experience to follow this workflow.

---

## 📦 Downloads

- **[pyem by asarnow](https://github.com/asarnow/pyem)**  
  Conversion tool between cryoSPARC and RELION formats.

- **[Multi-Curve Fitting Scripts](https://github.com/PengxinChai/multi-curve-fitting)**  
- **[Tubulin Lattice Subtraction Scripts](https://github.com/PengxinChai/tubulin-lattice-subtraction)**

Clone the scripts:

```bash
git clone https://github.com/PengxinChai/multi-curve-fitting
git clone https://github.com/PengxinChai/tubulin-lattice-subtraction
```

---

## 🔧 Preprocessing in cryoSPARC

1. Run cryoSPARC or cryoSPARC Live to preprocess your data.
2. Pick MT particles (template matching) and run 2–3 rounds of 2D classification.
   - Use MT templates
   - Diameter: `320Å`
   - Distance ratio: `0.25` (for 8nm particles)
   - Box size: `512`, downsample to `128` (bin4)
3. Select clean MT 2D classes.

---

## 🔁 Convert cryoSPARC to RELION `.star`

```bash
csparc2star.py --swapxy --relion2 particles_selected.cs JXX_passthrough_particles_selected.cs particles_selected.star
```

⚠️ Note: `--swapxy` and `--relion2` depend on your `pyem` version.  
Ensure the output `.star` file **does NOT contain optics groups**.

---

## 📁 Organize Micrographs

```bash
mkdir ori_mics sub_mics
mv motioncorrected/*doseweighted.mrc ori_mics
cd ori_mics
cp ../../JXX/particles_selected.star .
```

---

## 🔄 Recenter Coordinates

```bash
star_origin0_scale.com 4 particles_selected.star
```

- Use `4` for bin4 (e.g. 512 → 128), `2` for bin2.

---

## 🧩 Split STAR per Micrograph

```bash
star_split.py particles_selected_origin0.star *doseweighted.mrc
```

---

## 🖼️ Check Coordinates with RELION

```bash
relion_display --pick   --i XXX_patch_aligned_doseweighted.mrc   --coords XXX_patch_aligned_doseweighted_split.star   --scale 0.3 --black 0 --white 0   --sigma_contrast 3 --particle_radius 46   --lowpass 20 --highpass 2000 --angpix 0.8
```

---

## 🧮 Multi-Curve Fitting

```bash
mcurve_fitting_2D.py --pixel_size_ang 0.868 --poly_expon 2 XXX_split.star
```

Verify with:

```bash
relion_display --pick   --i XXX_patch_aligned_doseweighted.mrc   --coords XXX_patch_aligned_doseweighted_split_resam_Zscore.star   --scale 0.3 --black 0 --white 0   --sigma_contrast 3 --particle_radius 46   --lowpass 20 --highpass 2000 --angpix 0.8
```

---

## 🔍 Segment MTs into Small Pieces (Singlets Only)

```bash
split_segments.py XXX_split_resam_Zscore.txt
```

➡️ Produces ~20 coords/segment (≈80nm).  
Output: `split_resam_Zscore_renumber.txt`

---

## 🎭 Prepare MT Mask

```bash
cp common_masks/XXX.mrc .
relion_image_handler --i MT-250A_mask_angpix1A_box400X40.mrc   --o MT-250A_mask_angpix0.8A.mrc   --rescale_angpix 0.8
```

---

## 🧹 Subtract MT Signal (Large Scale)

```bash
cp mrc_2d_curve_weaken_one.sh .
chmod +x mrc_2d_curve_weaken_one.sh
./mrc_2d_curve_weaken_one.sh XXX_doseweighted.mrc
```

Check results using **IMOD** or **RELION**.

### Parallel Subtraction (Python 2 Required)

```bash
python2 para_run.py 32 ./mrc_2d_curve_weaken_one.sh XXX*_doseweighted.mrc
```

Or write your own bash script for batch processing.

---

## 📂 Finalize Subtracted Micrographs

```bash
mv ori_mics/*sub.mrc sub_mics
rename sub.mrc .mrc sub_mics/*sub.mrc
cd motioncorrected
ln -s ../sub_mics/*doseweighted.mrc .
ln -s ../ori_mics/*doseweighted.mrc .
```

⚠️ Linking original micrographs ensures cryoSPARC won’t fail due to missing MTs.

---

## 🚀 Continue Processing in cryoSPARC

Use the new micrographs in your next cryoSPARC pipeline steps (e.g., re-extraction, refinement, etc).
