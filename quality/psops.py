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


class LSST_Obs(object):
    def __init__(self, mjd_center, lsstrequirements, ra=0., dec=0.,
                 timeWindow=[-30., 50.]):
        self.requirements = lsstrequirements
        self.bumpFactors = self.requirements['bF']
        self.timeWindow = timeWindow
        self.ra = 0.
        self.dec = 0. 
        self.mjd_center = mjd_center
        self.fieldID = 1


    @property
    def meanNumObsperBand(self):
        """
        Mean number of observations in bands given the bumpfactors
        over the LSST Requiements
        """
        return meanNumObservation(self.requirements,
                                  self.bumpFactors,
                                  self.timeWindow)


    @property
    def uniformlySpacedEvents(self):        
        """
        Uniformly placed observations in the timeWindow in each band
        given the correct bumpFactor and LSST requirements
        """
        meanObs = self.meanNumObsperBand
        return uniformlySpaced(events=meanObs,
                               mjd_center=self.mjd_center,
                               mjd_window=self.timeWindow)


    @property
    def Observations(self):
        """
        """
        self._observations = self.uniformlySpacedEvents
        return self._observations 

    def add_depth(self, obs):
        """
        """
        depths =  self.requirements['medianSVD'].ix[obs['band']]
        obs['fiveSigmaDepth'] = depths.values
        return obs


    def obsValues(self):
        """
        `pandas.DataFrame` including all values
        """

        obs = self.Observations
        obs['ra'] = self.ra
        obs['dec'] = self.dec
        self.add_depth(obs)
        obs.rename(columns={'MJD': 'expMJD', 'band':'filter'}, inplace=True)
        obs['fieldID'] = int(self.fieldID)
        obs['night'] = np.floor(obs.expMJD.values)

        return obs


    
