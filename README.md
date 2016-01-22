# Cadence :  A repository to study cadence requirements for LSST and associated projects

## Packages

### gedankenLSST
The aim of this package is to perform a thought experiment producing a set of LSST observations, and utilize those observations to explore how astrophysical objects might be observed. The LSST operations simulator (OpSim) uses a historical dataset of weather, modules to calculate quantity from such data by treating it as a realization, and a scheduler which can schedule LSST observations meeting variious requirements and attempting to optimize certain functions. Unlike OpSim, the goal of this package is *NOT* to schedule or optimize any function. Instead, it will blindly have observations at times, bands and locations that are specified, and return outputs of observed times, bands, and fivesigmadepths in a format similar to OpSim (but not having other columns in the usual OpSim output) as a `pandas.DataFrame`. The goal is to use the same functions used by OpSim to do these calculations (not yet achieved) and therefore ultimately obtain the values reported by OpSim if one requests visits from OpSim 

This is largely intended for use at individual locations (fields), and for SNe. 

#### Requirments:
- [lsst.sims.catUtils](https://github.com/lsst/sims_catUtils) package must be setup. [Installation instructions are here](https://confluence.lsstcorp.org/display/SIM/Catalogs+and+MAF). Currently the branch sniacatsim_rebase must be setup.
- [OpSimSummary](https://github.com/rbiswas4/OpSimSummary) with installation instruction in README
#### Examples:

- [Basic Usage :](./examples/using_gedankenLSST.ipynb) 
