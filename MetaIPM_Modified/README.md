# MetaIPM: A Meta-population Integral Projection Model


#### Authors:          Richard A. Erickson, James P. Peirce, and Gregory J. Sandland
#### Point of contact: Richard A. Erickson (rerickson@usgs.gov)
#### Repository Type:  Formal _Python_ language package
#### Year of Origin:   2021 (original publication)
#### Year of Version:  2021
#### Version:          1.0.0 
#### Digital Object Identifier (DOI): https://doi.org/10.5066/P9PW673G
#### USGS Information Product Data System (IPDS) no.: IP-124176 (internal agency tracking)

***

_Suggested Citation:_

Erickson, RA, Peirce JP, and Sandland, GJ. 2021.
MetaIPM: A Meta-population Integral Projection Model.
Version 1.0.
U.S. Geological Survey software release. Reston, Va.
https://doi.org/10.5066/P9PW673G.

_Authors' [ORCID](https://orcid.org) nos.:_

- Richard A. Erickson, [0000-0003-4649-482X](https://orcid.org/0000-0003-4649-482X);
- James P. Peirce, [0000-0002-7147-3695](https://orcid.org/0000-0002-7147-3695)
- Gregory J. Sandland, [0000-0002-9716-0232](https://orcid.org/0000-0002-9716-0232)


***
***

# Package overview and purpose

`MetaIPM` is a `Python` package (Python Software Foundation 2020) that models meta-population dynamics and continuous growth rates via an integral projection model (IPM) for species living in distinct habitat patches.
The package stems from a model that compares invasive carp population control strategies (Erickson et al. 2018).
For example, Erickson et al. (2017) used an R predecessor version of this model to examine how YY-males could be used to control grass carp.
The package supports differing sex and any organisms living in distinct habitat patches.

`MetaIPM` relies on multiple ecological theories.
The spatial component of the meta-population theory relies on discrete habitat patches (nodes) and connections (paths) between the patches, as described in Taylor and Norris (2010).
The continuous growth modeling of individuals' size was designed to capture growth of fishes. Ellner et al. (2016) describe the theory of IPMs.
Furthermore, our model implementation will serve as a starting place for other people seeking to implement a custom IPM.
Lastly, our model captures the full-annual cycle (FAC) of the model organisms. FAC models attempt to capture all the habitat used by a particular species across seasons.
Holstetler et al. (2015) provide an overview of models relying on FACs.

More of the model's underlying theory and application are described in
the Jupyter Notebooks included as a part of this Repository.
Specifically, the `Model_overview` notebook in the `Tutorial` folder.

# Data requirements

Please see the `Model_inputs` notebook in the `Tutorial` folder.

# Package installation and requirements

## Requirements

MetaIPM was created with Python version 3.7 and has been used with Python 3.8.
The following Python packages are required:

- `setuptools` for installing MetaIPM
- `matplotlib` for plotting results
- `seaborn` for plotting results
- `numpy` for arrays and numerical methods
- `pandas` for DataFrames and similar methods
- `scipy` for probability functions

These packages may be installed via `pip` or your local Python install
methods.
A `conda` environment file, `meta.yml`, is also provided.
The `conda` environment [documentation][Conda_yml] describes how to
use this file.

This package takes less than 1 minute to build on a Surface Pro 7 running
Windows 10 with an Intel(R) Core(TM) i7-1065G7 CPU @ 1.30GHz.
The tests take about 2 minutes on the same system.

After downloading MetaIPM, the package may be installed via a terminal by running 

```{bash}
python setup.py install sdist bdist_wheel
```

Depending upon your local Python configuration, you may need to use
`python3` in place of `python`.
This method is further described in the Packaging Projections [Python
tutorial][Package_tutorial]

The tutorials for this package also use Jupyter Notebooks.
The Jupyter project's [homepage][Jupyter_home] describes how to
install and use Jupyter Notebooks.

## Steps for novice Python users

These directions are for novice Python users looking for quick start direcitons.

1. Download Miniconda from the [Miniconda webpgae][Miniconda]. This provides you with a working version of Python. USGS Windows users can currently install this without IT.
2. Open the Miniconda terminal.
3. Install JupyterLab following the directions on [JupyterLab webpage][JupyterLab] following the linked directions in the Miniconda terminal.
4. Use `conda install <package name>` to install all of the required packges listed in the previous section (e.g., `conda install matplotlib`).
5. Download this repository in the conda terminal using `git clone https://code.usgs.gov/umesc/quant-ecology/metaipm.git` **Note:** You may want to use a different git address if you want a specific version of the package.
6. Change directories in the terminal into the downloaded (_cloned_) folder using `cd metaipm`.
7. Install this package by typing `python setup.py install sdist bdist_wheel` 
8. Launch JupyterLab by typing `jupyter lab` and then use the GUI to navigate to the `Tutorials` folder and open the tutorial Notebooks. 


# Repository Files

This repository contains the following folders and files:

- `README.md` is this file.
- `LICENSE.md` is the Official USGS License. 
- `code.json` is the code metadata.
- `CONTRIBUTING.md` describes how to contribute to this project.
- `DISCLAIMER.md` is the standard USGS disclaimer.
- `.gitignore` is a file telling git which files to not track.
- `setup.py` is a file used to install the package by typing `python setup.py install sdist bdist_wheel`
- `MetaIPM` contains the Python package's files.
- `meta.yml` will create a conda environment in which this package may be installed.
- `Tutorial` contains model documentation in Jupyter Notebooks:
  - `Model_overview.ipynb` provides an overview of the model and the model's implementation in Python. This is the recomended start file.
  - `Model_input_files.ipynb` describes the model's input files
  - `Deterministic_example.ipynb` demonstrates a deterministic example of the model
  - `Stochastice_exampele.ipynb` demonstrates a stochastic example of the model
- `tests` contains unit tests for testing this package. These files may be run by typing `python -m unittest` using the terminal within this directory.

# Acknowledgments

Professor KR Long from Texas Tech University provided the initial ideas for using object-orientated programming for the network model.
D. Glover (currently Illinois DNR) and JL Kallis (US Fish and Wildlife Service) provided input for the initial development of this model and appliation to fisheries managment.
This research was funded by the USGS Invasive Species Program, Great Lakes Restoration Initiative, and through the Habitat for Migratory Species working group at National Institute for Mathematical and Biological Synthesis (NIMBioS) through Cooperative Agreement #DBI-1300426 between the National Science Foundation and the University of Tennessee, Knoxville.

# USGS Product Disclaimer

Any use of trade, firm, or product names is for descriptive purposes only and does not imply endorsement by the U.S. Government.

# References

Ellner SP, Childs DZ, Rees M. (2016). _Data-driven modelling of
structured populations. A practical guide to the Integral 
Projection Model_. Springer: New York.

Erickson RA, Eager EA, Brey MK, Hansen MJ, and Kocovsky, PM. (2017). An
integral projection model with YY-males and application to evaluating
grass carp control. _Ecological Modelling_, 361,
14-25. https://doi.org/10.1016/j.ecolmodel.2017.07.030

Erickson RA, Eager EA, Kocovsky PM, Glover DC, Kallis JL, and Long KR
(2018). A spatially discrete, integral projection model and its
application to invasive carp. _Ecological Modelling_, 387,
163-171. https://doi.org/10.1016/j.ecolmodel.2018.09.006

Hostetler JA, Sillett TS, Marra PP, (2015). Full-annual-cycle
population models for migratory birds. _Auk_ 132, 433-449.

Python Software Foundation. (2020). Python Language Reference,
version 3. URL https://www.python.org

Taylor CM and Norris DR. (2010). Population dynamics in
migratory networks. _Theoretical Ecology_, 3, 65-73.

[Conda_yml]: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file
[Jupyter_home]: https://jupyter.org/
[Package_tutorial]: https://packaging.python.org/tutorials/packaging-projects/
[TRACE_home]: https://cream-itn.eu/trace
[Miniconda]: https://docs.conda.io/en/latest/miniconda.html
[JupyterLab]: https://jupyter.org/install.html
