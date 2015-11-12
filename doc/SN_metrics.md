# Discussion of SN Metric

## What we need to do
- Quantify the potential of SN cosmology as a function of survey strategy
- This is not an optimization task, where we try to understand what the best survey strategy for SNIa cosmology is. rather this has to evaluate how the SN cosmologgy analysis performs as a function of strategies, no matter how poor. 

### We have a method to compute a figure of merit averaged for a single SN given observations in a time window around it
Here we outline how the metric will work for each SN: we will refer to this as a per SN metric. We then outline how to use this to build a MAF metric which will grade the entire survey.
#### Potential for SN Cosmology performance:
- Roughly speaking, this implies the kind of constraints that one would obtain for the equation of state parameter 'w' of dark energy through SN Cosmology analysis. 
- An example would be to use the DETF figure of merit, where a particular model of dark energy allowing 'w' to vary with redshift in a particular way is chosen, and the metric is the inverse of the area of a contour in the two parameters 'w_0', and 'w_a' required to characterize 'w', marginalized over all the model parameters. This is an example and therefore definite, and one could have different examples. But the full analysis would still require having multilpe realizations of the entire survey. Moreover, this is also not completely definite, since the underlying realization of cosmology (among other things) could change this metric.

#### Use some intuition to convert this into a quality per supernova:
- We know that the likelihood for cosmology looks roughly like Delta mu^T C^{-1} Delta mu, Where Delta mu = estimated(mu) - mu(cosmology), and C is roughly diagonal where the diagonal elements are of the form sigma(mu)^2 + sigma(intrinsic)^2. So, we can base the quality of light curve metric for a particular SN as min(sigma(intrinsic)^2/sigma(mu)^2, 1). sigma(intrinsic) is usually of the order 0.1. We will take this to be 0.8. 
- We calculate sigma(mu) from fits using linear propagation of the errors from the light curve model parameters to sigma(mu)
- We can multiply this by a discovery metric (reasonably easy)
- We can mulitply this by a classification metric (not clear .... but hopefully will come up) 
- As a product: this gives the total usability of a SN given the observations around its time of peak. Note location on sky is also an input; it determines MW extinction and therefore the SNR which enters the different metrics

In summary this will be the API of the per SN metric:
Input: SN paramters, location/MW extinction, Observations around the SN peak
Output: a number in [0., 1.]. 1 => perfectly utilized, 0. => completely useless.

** Note: the per SN metric calculation is slow **

#### The MAF metric: Grading Observational Strategy in MAF using metric
How will this per SN metric be used to grade an observing strategy? 
- The input to the MAF metric will be an observing strategy (eg. OpSim output) (This is usual)
- MAF will go to each healpixel covering the sky and try to compute a SN metric for that healpixel
- At each healpixel, instantiate a number of random numbers which represent the explosion times of all the SN during the survey. This number is ~ few thousand for each pointing.
- Add z values to each of them according to an input SN rate.
- Set the model parameters to the simplest Mb = -19.5, x1 = 0.  c=0. 
- Calculate MWEBV for the healpixel from SFD dust maps
- For each SN, find observations in the time window, calculate the per SN metric
- Compute the number sum (per SN metrics weight(z)) /num(SN) , where weight(z) = 1 (in the simple case). We may want to change this as different redshift distributions have different impacts on cosmological parameter detection, but let us try keeping it at 1. (Maybe train this later using simulations)
- Evaluate this as the SN metric for that patch of sky. 

#### This works, but is too slow (and MAF will require fitting etc.)
So the way out is to build a function that will emulate the behavior of the per SN metric, but do it fast. We will call such a function 'emulator' since that is already the prevelant terminology in cosmology. For our purposes, an emulator is a pair (training set, machine learning/ interpolating strategy). 
- In particular, the problem would be solved if we used a training set which computed the per SN metric for every kind of observing strategy. But this is impossible because there are too many such observing strategy over a 100 day period.
- Given the fact that SN light curves vary very little over the period of a single day, we suggest using a representation for the space where we calculate the number of observations in each filter in each day. So the this is the number of values in each of Ncell = 600 cells.
- Next, we realize that there are constraints on total time. Fixing the total number of visits to these Ncell cells to Nvisits, the number of possible configurations is 
(Ncell + Nvisits -1) C Ncell. For the  main fields where the NVisits averages to 800-1000 over 10 years, the average number for 100 days is about 1000 X 100 / 3650. For Deep Fields this number is 25 times larger. 
- More clearly, this means that we have a function that maps a domain to a field, but want to only compute that function for a sub-domain, and use intuition/statistical methods to emulate the function behavior in other regions of the domain.
- Slightly different from Dimensional Reduction, because we cannot run all the cases.
