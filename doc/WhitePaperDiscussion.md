# Supernova Cosmology and Astrophysics

## Science Goals of the Supernova Group

* Supernova Cosmology: Use a sample of well-measured supernovae and past knowledge of supernovae behavior to obtain intrinsic brightnesses of supernovae and derive constraints on cosmology, particularly dark energy properties
* Related: Improvement of our understanding of the supernovae population. This 
includes understanding the distribution of SN properties in nature, and their correlation with their environments (host-galaxy properties, progenitor stars 
etc.)
* Use SN to study large scale structure, or deviations of the cosmology from 
FRW or certain galaxy populations. Largely, this is achieved by using SN as tracers of their host galaxies with the additional information about their distances being  well-measured.
* Lensing time delays measured using SN

* All of the stated goals stand to gain from increased numbers of well-measured supernovae. The first two goals, however, are indpendent of the spatial
positions of the supernovae, and do not necessarily gain if the same set of supernovae were distributed across a large region of the sky. The third goal, however, does require spatial coverage, and LSST is the only survey that could potentially do this.

To summarize, 

* Need a large number of SN
* Be able to detect SN candidates early enough for selective follow-up
* classify SN types and from other possible transients 
* Need a good determination of intrinsic brightness

The last two goals, classification and intrinsic brightness determination of SN Ia required for cosmology may have different cadence requirements for optimization. 

### Previous Studies

Based on previous simulation studies based on older versions of OpSims, the WFD  proposal has yielded few SN of useful quality. These studies have not looked into regions of overlap between field pointings (and doing so with and without dithers) is an important aspect of this study.
  
## Requirement for these goals

* High precision calibrated flux measurement of mulitband supernova light curve
* 'Good' temporal and wavelength (ie. number of filters) sampling of the light curve of each supernova. The sampling over multiple filters is useful as determination of SNIa intrinsic brightness strongly depends on multi-band information to
 determine a color like quantity at a particular phase. 

We note that while a qualitative intuitive understanding of 'good sampling' exists (see below), we do not have a quantitative understanding of how the lack of such sampling degrades information. Outlining and carrying out such investigations should be an important part of this whitepaper.

## Observing Strategy Characteristics

* Should have large number of epochs
* Distributed in multiple filters (the appropriate filters depend on z)
* Should be sampled roughly uniformly in time
        
## Exploring OpSims Outputs:

* We can study the cadence distribution by filter from the OpSim output directly in each field. The plot below shows the number of visits (or 2 15 second exposures) done in a particular field in different filters per night during the first season of Enigma_1189 in a DDF with coordinates as described. The grid shows a 5 day period to guide the eye. 
![cadence in a season of Enigma 1189 in a field](images/cadence.png)
* We can study simulations of SN and apply classification and light curve fitting procedures to them in order to assess how well we can do with a simulated sample from OpSim. 
* We can look at improvements of light curve fits by varying the epochs from OpSim.
* We can compare this cadence to the cadence with which SN were observed in previous SN surveys.
* We currently have two metrics that can be used in MAF that pertain to SN. We should try to understand how these metric values correlate with gains in light curve fits or cosmology as the opsims strategy changes.
* It is unclear how to account for the fact that our knowledge of SNIa might improve over time leading to larger gains for better strategies. 
* It is also unclear if some of this will be accounted for by improvements in intrinsic dispersion.

## Cadence Metrics
Two cadence metrics for SN have been written by 
* Rick Kessler 
* Alex Kim https://github.com/DarkEnergyScienceCollaboration/surveymetrics

## Some issues

* Should the analysis be separate for DDF anf WFD strategies? A combined study potentially has more benefits in the DDF fields, but has the problem of tying the two proposals togther.
* The statements about sampling of the SN light curves in multiple bands above have been made in the context of determining intrinsic brightness of SNIa. Aside  from that, there may be requirements for obtaining good photometric redshifts of host galaxies (of course, these may be determined from subsequent spectroscopic follow-up of hosts as well). Will the photoz group supply us with information on this count, and if so, what information should we provide?
