import numpy as np
import pandas as pd

lsstBands = ['u', 'g', 'r', 'i', 'z', 'y']
LSSTReq = dict()
# Total Duration of survey in days
LSSTReq['Duration'] = 3650.
# Median Single Visit five Sigma Depth in mags 
LSSTReq['medianSVD'] = pd.Series([23.9, 25., 24.7, 24.,23.3, 22.1],
                                 index=lsstBands)
# Mean number of viists 
LSSTReq['meanNumVisits'] = pd.Series([56, 80, 184, 184, 160, 160],
                                     index=lsstBands, dtype=np.float)
# bumpFactors
LSSTReq['bF'] = pd.Series([1.]*len(lsstBands), index=lsstBands)



def meanNumObservation(lsstRequirements, bumpFactors=LSSTReq['bF'],
                       timeWindow=[-30, 50]):
    """
    returns the mean number of observations in each band, where the bands 
    u, g, r, i, z, y are indexed by the numbers 0, 1, 2, 3, 4, 5.
    in a time window.

    Parameters
    ----------
    bumpFactors : array of factors to bump up the number of visits in each
    band 
    lsstRequirements :
    timeWindow :
    """
    
    totalTime = lsstRequirements['Duration']
    timeHigh = timeWindow[1]
    timeLow = timeWindow[0]
    
    fractionalTime = (timeHigh - timeLow) / totalTime
    events = np.round(lsstRequirements['meanNumVisits'] * fractionalTime \
                      * bumpFactors)
    
    return events
    
def uniformlySpaced(events, mjd_center, mjd_window=[-30., 50.]):

    mjd_width = mjd_window[1] - mjd_window[0]
    deltaT = mjd_width/ (events + 1)
    mjd_low, mjd_high = np.array(mjd_window) + mjd_center
    TVals = {band: np.arange(mjd_low, mjd_high, deltaT[band])
              for band in deltaT.index}
    dflist = []
    for band, vals in TVals.items():
        df = pd.DataFrame({'MJD': vals})
        df['band'] = band
        dflist.append(df)

    df = pd.concat(dflist, ignore_index=True)
    return df
