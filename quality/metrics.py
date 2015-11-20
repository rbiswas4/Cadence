#!/usr/bin/env python

from OpSimSummary import summarize_opsim as oss
import matplotlib.pyplot as plt
import os
import numpy as np
import copy

from astropy.table import Table
from astropy.units import Unit
import sncosmo

from lsst.sims.photUtils import BandpassDict
from lsst.sims.catUtils.mixins import SNObject
from astropy.utils.misc import lazyproperty
from efficiencyTable import EfficiencyTable


class PerSNMetric(oss.SummaryOpsim):
    def __init__(self, fieldID, t0, summarydf=None, snState=None, lsst_bp=None,
            efficiency=None):
        oss.SummaryOpsim.__init__(self, summarydf=summarydf)
        
        self.fieldID = fieldID
        self.t0 = t0
        self._lc = None
        self._numDropped = None
        self.snState = snState
        self.lsst_bp = lsst_bp
        self.efficiency = efficiency
        return

    @property
    def numDropped(self):
        return self._numDropped
    
    def lcplot(self, lowrange=-30., highrange=50.):
        lc = self.lightcurve
        data = Table(lc.to_records())
        sncosmo.plot_lc(data, model=self.sncosmoModel, color='k',
                        pulls=False)
        
    @property
    def sncosmoModel(self):
        return self.SN.equivalentSNCosmoModel()
    
    @property
    def lc(self):
        return self._lc
        
    @property
    def numVisits(self):
        return self.SNCadence[2]
        
    @property
    def numNights(self):
        return self.SNCadence[3]
        
    @property 
    def numFiltNights(self):
        return self.SNCadence[4] 


    @lazyproperty
    def SNCadence(self):
        fieldID = self.fieldID
        mjd_center = self.t0
        
        vals = self.cadence_plot(fieldID, mjd_center=mjd_center, mjd_range=[-30., 70.])
        return vals

    @property
    def SNCosmoLC(self):
        return Table(self.lightcurve.to_records())
        
    @property         
    def lightcurve(self, lowrange = -30., highrange=50. ):
        
        sn = self.SN
        #dataframe.set_index('obsHistID')
        # timewindowlow 
        timelow = sn.get('t0') + lowrange
        timehigh = sn.get('t0') + highrange
    
        # Model range
        modellow = sn.mintime()
        modelhigh = sn.maxtime()
    
        if modellow > timelow:
            timelow = modellow
        if modelhigh < timehigh:
            timehigh = modelhigh
        
        dataframe = self.simlib(fieldID=self.fieldID)
        
        _ = dataframe.query('expMJD > @timelow and expMJD < @timehigh')
        df = _.copy(deep=True)
        colnames = ['time', 'band', 'flux', 'fluxerr', 'zp', 'zpsys', 'SNR',
                    'finSeeing', 'airmass', 'filtSkyBrightness','fiveSigmaDepth',
                    'propID', 'night', 'DetectionEfficiency']
        df['band'] = df['filter'].apply(lambda x: x.lower())
        df['flux'] = df.apply(lambda row: sn.catsimBandFluxes(row['expMJD'],
                              self.lsst_bp[row['band']]), axis=1)
        df['fluxerr'] = df.apply(lambda row: sn.catsimBandFluxError(row['expMJD'],
                                 self.lsst_bp[row['band']],
                                 m5=row['fiveSigmaDepth']), axis=1)
        df['zp'] = 0.
        df['zpsys'] = 'ab'
        df.rename(columns={'expMJD':'time'}, inplace=True)
        os = len(df)
        df = df.query('flux > 0. and fluxerr > 0.')
        s = len(df)
        df['SNR'] = df['flux'] / df['fluxerr']

        df['DetectionEfficiency'] = df.apply(self.func, axis=1)
        df.sort('SNR', ascending=False, inplace=True)
        self._numDropped = os - s
        self._lc = df
        return df[colnames]
    
    @lazyproperty
    def fits(self):
        """
        `sncosmo.fit_lc` return which is a tuple to fit results, and sncosmo
        model set to best fit model.
        """
        return sncosmo.fit_lc(self.SNCosmoLC, model=self.sncosmoModel,
                        vparam_names=['t0', 'x0', 'x1', 'c'], minsnr=3.)


    def func(self, row):
        band = row['band']
        SNR = row['SNR']
        if self.efficiency is None:
            return np.nan
        else:
            return self.efficiency.effSNR(band, SNR)


    @property
    def deltamusq(self):
        """
        Parameters
        ----------
        fitCov: Covariance matrix arranged so that in order of x0, x1, c 
        x0 : Value of x0 parameter
        """
        alpha = 0.11
        beta = -3.1
        if self.fits is None:
            return None
        fitCov = self.fits[0].covariance[1:, 1:]
        cov = np.copy(fitCov)

        # Convert to mB , x1, c assuming linear propagation
        x0 = self.SN.get('x0')
        cov[:, 0] = -2.5 * fitCov[:, 0] / x0 / np.log(10.)
        cov[0, : ] = -2.5 * cov[0, :] / x0 / np.log(10.)

        const = np.array([1., alpha, beta])
        sigmasq = np.sum(const * np.sum(cov * const, axis=1), axis=0)

        return sigmasq
        
    @property
    def radeg(self):
        ra = self.ra(self.fieldID)
        return np.degrees(ra)
    
    @property
    def decdeg(self):
        dec = self.dec(self.fieldID)
        return np.degrees(dec)
    
    @property
    def SN(self):
        """
        `lsst.sims.catsim.SNObject` instance with peakMJD set to t0
        """

        if self.snState is not None:
            return SNObject.fromSNState(self.snState)

        sn = SNObject(ra=self.radeg, dec=self.decdeg)
        sn.set(t0=self.t0)
        sn.set(z=0.5)
        sn.set_source_peakabsmag(-19.3, 'bessellB', 'ab')


        return sn
    
    @staticmethod
    def SNobj(fieldID, t0, snState=None): 
        sn = SNObject(ra=np.degrees(so.ra(fieldID)), 
                  dec=np.degrees(so.dec(fieldID)))
        sn.set(t0=t0)
        sn.set(z=0.5)
        sn.set_source_peakabsmag(-19.3, 'bessellB', 'ab')
        return sn
    def discoveryMetric(self, trigger=1):
     	"""
	return the detection probability as a function of the single exposure
	efficiencies
       	"""
	efficiency = self.lightcurve.DetectionEfficiency.astype(float)
	if trigger > 1.:
	    raise ValueError('Trigger > 1 not implemented yet\n')
        # probability of not being detected visit by visit
	q = 1.0 - np.asarray(efficiency)


        #print type(q)
        #print q
	logq = np.log(q)
        # probability of no detection
	logpiq = logq.sum()
	piq = np.exp(logpiq)

	return 1.0 -  piq
    
    def qualityMetric(self, Disp=0.05):
        
        return Disp * Disp / self.deltamusq


