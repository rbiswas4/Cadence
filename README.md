# Cadence :  A repository to study cadence requirements for LSST and associated projects

## Packages

### gedankenLSST
The aim of this package is to perform a thought experiment producing a set of LSST observations, and utilize those observations to explore how astrophysical objects might be observed. The LSST operations simulator (OpSim) uses a historical dataset of weather, modules to calculate quantity from such data by treating it as a realization, and a scheduler which can schedule LSST observations meeting variious requirements and attempting to optimize certain functions. Unlike OpSim, the goal of this package is *NOT* to schedule or optimize any function. Instead, it will blindly have observations at times, bands and locations that are specified, and return outputs of observed times, bands, and fivesigmadepths in a format similar to OpSim (but not having other columns in the usual OpSim output) as a `pandas.DataFrame`. The goal is to use the same functions used by OpSim to do these calculations (not yet achieved) and therefore ultimately obtain the values reported by OpSim if one requests visits from OpSim 

This is largely intended for use at individual locations (fields), and for SNe. 

#### Pre-requisites and Installation:
This is a python package and depends on many python packages, which are easily installable through pip or conda. Installing pandas would install other python packages required except the other two listed. 
- [pandas](http://pandas.pydata.org/) which is easy to install via conda or pip 
- [lsst.sims.catUtils](https://github.com/lsst/sims_catUtils) package must be setup. [Installation instructions are here](https://confluence.lsstcorp.org/display/SIM/Catalogs+and+MAF). Currently the branch sniacatsim_rebase must be setup.
- [OpSimSummary](https://github.com/rbiswas4/OpSimSummary) with installation instruction in README

Finally, while, not a requirement, some of the examples are in ipython/jupyter notebooks. To run these, you will need [jupyter Notebooks](http://jupyter.org/) which are also easy to install via conda or pip. 

Once the pre-requisites are installed, clone this repository and at the top level directory use the setup script to install the packages:
```
git clone https://github.com/rbiswas4/Cadence.git
cd Cadence
python setup.py install --user
```

#### Examples:

- [Basic Usage :](./examples/ExampleLightCurve_DDF_WFD.ipynb)
