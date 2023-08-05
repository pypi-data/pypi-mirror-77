# IIT MMS - Nikon collaborative Project N.5

This library constains the source code for various Image Scanning Microscopy (ISM) pixel reassignment methods, single and multi-image deconvolution, Fourier ring correlation analysis etc. New functionality will be integrated as the project proceeds. The release is based on our Microscope Image Processing Library (*MIPLIB*) library, which is licensed under BSD open source license. Please refer to the *License* file for details. 

## How do I install it?

I would recommend going with the *Anaconda* Python distribution, as it removes all the hassle from installing the necessary packages. The library should work on all platforms (Windows, MacOS, Linux), except for the CUDA GPU acceleration, which is not currently supported on macOS.


### Here's how to setup your machine for development:

  1. There are some C extensions in *miplib* that need to be compiled. Therefore, if you are on a *mac*, you will also need to install XCode command line tools. In order to do this, Open *Terminal* and write `xcode-select --install`. If you are on *Windows*, you will need the [C++ compiler](https://wiki.python.org/moin/WindowsCompilers)

  2. The Bioformats plugin that I leverage in MIPLIB to read microscopy image formats requires Java. Therefore, make sure that you have JRE installed if you want to use the bioformats reader.  Also make sure that the JAVA_HOME environment variable is set. You may also have to add the JAVA_HOME to your PATH. More info on that can be found here: [JPYPE](https://jpype.readthedocs.io/en/latest/install.html). 

3. Fork and clone the *MIBLIB* repository. The code will be saved to a sub-directory called *miplib* of the current directory. Put the code somewhere where it can stay. You may need to generate an SSH key, if you have not used GitLab previously.

4. Go to the *miplib* directory and create a new Python virtual environment `conda env create -f environment_nocuda.yml`. Alternatively use `environment.yml`, if you want to use GPU acceleration with image deconvolution (please see About GPU acceleration below). 

5. Activate the created virtual environment by writing `conda activate miplib`

6. Now, install the *miplib* package to the new environment by executing the following in the *miplib* directory `python setup.py develop`. This will only create a link to the source code, so don't delete the *miplib* directory afterwards. 

## How do I use it?

My preferred tool for explorative tasks is Jupyter Notebook/Lab. Please look into the notebooks/ folder for examples on ISM image reconstruction, FRC measurements (and other things). There is also a batch processing script for ISM pixel reassignment that can be invoked by `miplib.ism all <directory>`, where directory refers to a directory that contains your data files. The script automatically processes every compatible file in the directory. Our Carma *.mat* files as well as Zeiss AiryScan files are both supported. The reconstruction currently only works with 2D images. 

## Regarding Python versions

I recenly migrated MIPLIB to Python 3, and have no intention to maintain backwards compatibility to Python 2.7. You can checkout an older version of the library, if you need to work on Python 2.7.

## About GPU acceleration

The deconvolution algorithms can be accelerated with a GPU. On MacOS the CUDA GPU acceleration currently does not work, because there are no NVIDIA drivers available for the latest OS versions. For that reason I have included an environment file that does not install the CUDA specific packages. At some point in future I will hopefully have some time to add GPGPU support (e.g. through [Reikna](https://github.com/fjarri/reikna)).

## Publications

Koho, S. V. et al. Two-photon image-scanning microscopy with SPAD array and blind image reconstruction. Biomed. Opt. Express, BOE 11, 2905–2924 (2020)

[Koho, S. *et al.* Fourier ring correlation simplifies image restoration in fluorescence microscopy. Nat. Commun. 10 3103 (2019).](https://doi.org/10.1038/s41467-019-11024-z)

Castello, M. *et al.* A robust and versatile platform for image scanning microscopy enabling super-resolution FLIM. *Nat. Methods* **16**, 175–178 (2019)