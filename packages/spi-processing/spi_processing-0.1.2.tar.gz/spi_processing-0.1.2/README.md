# Installation

Processing scripts require **Python 3.6** or higher.

You can install stable version by:
```
pip install spi-processing
```

To install from git, clone the repository and use:
```
cd spi_processing
pip install .
```

# Hit processing

This section describe scripts for processing of diffraction images in CXI format.

## Compute photons number

Calculate number of photons and number of litpixels for every frame in CXI files.
Results are saved in datasets **num_photons** and **num_litpixels**.

```
spi_compute_photons.py [-h] [-o OUTPUT_DIR] FILE [FILE ...]
```

Options:
* `-o OUTPUT_DIR` - store results in provided folder with the same filenames. Otherwise, data will be added to input files inplace.

## Combine data

Combine multiple CXI files into single file.
Combine inner CXI structure when possible.
Arrays with same path in different files are concateneted along first dimention.

```
spi_combine.py [-h] -o OUTPUT_FILE FILE [FILE ...]
```

CXI files should include one or multiple image groups with path `/entry_1/image_n` .
Image groups from input files will be combined into one image group in output file if they include same `mask` and `image_center` datasets. 

## Filter data

Filter data in CXI file by values in some dataset. Other datasets are filtered if they have the same first dimension as filtering dataset.

```
spi_filter.py [-h] -d DSET [-o OUTPUT_DIR] [--outfile OUTPUT_FILE] [-m MIN_VALUE] [-M MAX_VALUE] [-r REPORT] FILE [FILE ...]
```

Options:
* `-d DSET` - path to dataset within `/entry_1/image_n/` groups.
* `-m MIN_VALUE`, `-M MAX_VALUE` - minimun and maximum allowed values in  dataset, ends are included.
* `-o OUTPUT_DIR` - store results in provided folder with the same filenames. Alternative is `--outfile OUTPUT_FILE` to combine filtered data into single file.
* `-r REPORT` - generate PDF report.

## Plot histogram

Create PDF histogram of values in dataset in one or many CXI files.

```
spi_plot_histogram.py [-h] -d DSET [-r START:END] [-s START:END] [-b BINS] [-o OUTPUT_FILE] FILE [FILE ...]
```

Options:
* `-d DSET` - path to selected dataset within `/entry_1/image_n` groups. Data in all image groups in all files will be concatenated.
* `-r START:END` - set range of histogram values
* `-s START:END` - add selection box between values
* `-b BINS` - number of histogram bins
* `-o OUTPUT_FILE` - name of output PDF file.

## Correct background

Correct background scattering in CXI files by analysis of intensity distribution.

```
spi_correct_background.py [-h] [-o OUTPUT_DIR] [-M MAX] [-O OVERFLOW] [-r REPORT] [--no-correct] FILE [FILE ...]
```

Options:
* `-o OUTPUT_DIR` - store results in provided folder with the same filenames. Otherwise, input files will be corrected inplace.
* `-M MAX` - maximum possible background intensity, affects performance.
* `-O OVERFLOW` - do not correct intensities above OVERFLOW value.
* `-r REPORT` - generate PDF report.
* `--no-correct` - do not prosess data, only generate report by comparison of data in input files and *existing* files in OUTPUT_DIR.

## Estimate center

Estimate center of diffraction images from scattering data.
Estimation is based on rotational symmetry of averaged image.
Results are saved into `image_center` dataset.

```
spi_estimate_center.py [-h] [-o OUTPUT_DIR] [-s] [-r REPORT] FILE [FILE ...]
```

Options:
* `-o OUTPUT_DIR` - store results in provided folder with the same filenames. 
Otherwise, `image_center` dataset will be added to input files.
* `-s` - all input files are considered to have the same beam position.

## Refine center

Refine values of `image_center` by correlation with simulated sphere scattering. For correct result, average frame should have dictinct fringes (frames should have tight range of particle sizes).
Input files must include `image_center` data that is used as starting point.

```
spi_refine_center.py [-h] [-o OUTPUT_DIR] [-s] [-r REPORT] [--max-shift MAX_SHIFT] [-R RADIUS] -w WAVELENGTH -d DISTANCE --pix PIXEL FILE [FILE ...]
```

Options:
* `-o OUTPUT_DIR` - store results in provided folder with the same filenames. Otherwise, `image_center` dataset will be updated in input files.
* `-s` - all input files are considered to have the same beam position.
* `--max-shift MAX_SHIFT` - maximum distance between old and new positions in pixels.
* `-R RADIUS` - maximum considered radius of simulated scattering pattern (pixels). Data outside this radius do not affect result.
* `-w WAVELENGTH` - radiation wavelenght (Angstrom).
* `-d DISTANCE` - detector distance (m).
* `--pix PIXEL` - pixel size (m).

## Set center position

Set specific value of `image_center` in CXI file.

```
spi_set_center.py [-h] [-o OUTPUT_DIR] [-x CENTER_X] [-y CENTER_Y] [-z CENTER_Z] [-i FILE] FILE [FILE ...]
```

Options:
* `-o OUTPUT_DIR` - store results in provided folder with the same filenames. Otherwise, `image_center` dataset will be updated in input files.
* `-x CENTER_X`, `-y CENTER_Y` and `-z CENTER_Z` - `image_center` values. Alternatively, `-i FILE` can be provided to copy value of `image_center` from file.

## Estimate size

Estimate size of particles in data by fitting power spectral density (PSD) against spherical form factor.
Input files must include `image_center` data.

Inside each `image` group, new `psd` group will be created with datasets:
* **data** - PSD values for each frame
* **size** - estimated particle size for each frame
* **scale** - estimated intensity scale for each frame
* **size_score** - fidelity score of size estimation.
* **size_range** - tested range of particle sizes
* **fit_diff** - difference between PSD and each spherical form factor for each frame.

```
spi_estimate_size.py [-h] [-o OUTPUT_DIR] [-p PERCENTAGE] [-m S_MIN] [-M S_MAX] [-r R_MIN] [-R R_MAX] -w WAVELENGTH -d DISTANCE --pix PIXEL [-i INTERP] [-n NSIZE] [--icosahedron] FILE [FILE ...]
```

Options:
* `-o OUTPUT_DIR` - store results in provided folder with the same filenames. Otherwise, `image_center` dataset will be updated in input files.
* `-p PERCENTAGE` - use only brightest fraction of angular data for PSD estimation.
* `-m S_MIN` and `-M S_MAX` - range of sphere sizes in Angstrom, `-n NSIZE` of equally distributed sizes will be tested against each frame.
* `-r R_MIN` and `-R R_MAX` - area on frames between R_MIN and R_MAX (pixels) will be considered for size estimation.
* `-w WAVELENGTH` - radiation wavelenght (Angstrom).
* `-d DISTANCE` - detector distance (m).
* `--pix PIXEL` - pixel size (m).
* `-i INTERP` - number of sphere form factor points per 1 pixel. Allow to reduce errors for fringe size ~3 pixels and lower.
* `-n NSIZE` - Number of sizes tested within size range.
* `--icosahedron` - Size of particle will be computed with assumption that it is a regular icosahedron.
