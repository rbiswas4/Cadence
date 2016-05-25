import numpy as np
import pandas as pd
from lsst.sims.catUtils.supernovae import SNObject
from opsimsummary import summarize_opsim as oss
from astropy.table import Table

__all__ = ['SNObs']
class SNObs(oss.SummaryOpsim):

    def __init__(self, t0, fieldID=None, raCol=None, decCol=None, ra=0.,
                 dec=0., peakabsmagBessellB=-19.3,
                 summarydf=None, snState={'z':0.5}, lsst_bp=None):

        oss.SummaryOpsim.__init__(self, summarydf=summarydf)
        self.fieldID = fieldID
        self.raCol = raCol
        self.decCol = decCol
        self._ra = np.radians(ra)
        self._dec = np.radians(dec)
        self.summary = summarydf
        self._peakabsmagBessellB = peakabsmagBessellB
        self.t0 = t0
        self._lc = None
        self._numDropped = None
        self._snState = snState
        self.lsst_bp = lsst_bp
        self.lowrange = -30.
	self.highrange = 50.


    @property
    def radeg(self):
        if self._ra != 0. and self._dec != 0.:
            return np.degrees(self._ra)
        if self.fieldID is not None:
            ra = self.ra(self.fieldID)
        elif self.raCol is not None:
            ra = self.summary[self.raCol].iloc[0]
        else:
            ra = self._ra
        return np.degrees(ra)

    @property
    def decdeg(self):
        if self._dec != 0. and self._dec != 0.:
            return np.degrees(self._dec)
        if self.fieldID is not None:
            dec = self.dec(self.fieldID)
        elif self.decCol is not None:
            dec = self.summary[self.decCol].iloc[0]
        else:
            dec = self._dec
        return np.degrees(dec)

    @property
    def snState(self):
        if self.SN.SNstate is None:
            SNstate = self._snState
        else:
            SNstate = self.SN.SNstate
        return SNstate


    @snState.setter
    def snState(self, value):
        self._snState = value
        return self._snState

    @property
    def SN(self):
        """
        `lsst.sims.catsim.SNObject` instance with peakMJD set to t0
        """

        #if self.snState is not None:
        #    return SNObject.fromSNState(self.snState)

        sn = SNObject(ra=self.radeg, dec=self.decdeg)
        sn.set(t0=self.t0)
        sn.set(**self._snState)
        sn.set_source_peakabsmag(self._peakabsmagBessellB, 'bessellB', 'ab')

        return sn


    def SNCosmoLC(self, scattered=False, seed=0):

        lc = self.lightcurve
        lc['modelFlux'] = lc['flux']

        # add scatter if desired
        np.random.seed(seed)
        lc['deviation'] = np.random.normal(size=len(lc['flux']))

        if scattered:
            lc['flux'] = lc['flux'] + lc['deviation'] * lc['fluxerr']

        return Table(lc.to_records())
    
    @property
    def lightcurve(self, lowrange=-30., highrange=50. ):

        sn = self.SN
        # dataframe.set_index('obsHistID')
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

        if self.fieldID is None:
            dataframe = self.summary
        else:
            dataframe = self.simlib(fieldID=self.fieldID)

        x = dataframe.query('expMJD > @timelow and expMJD < @timehigh')
        df = x.copy(deep=True)
        colnames = ['time', 'band', 'flux', 'fluxerr', 'zp', 'zpsys', 'SNR',
                    'finSeeing', 'airmass', 'filtSkyBrightness','fiveSigmaDepth',
                    'propID', 'night', 'DetectionEfficiency']
        df['band'] = df['filter'].apply(lambda x: x.lower())
        df['flux'] = df.apply(lambda row: sn.catsimBandFlux(row['expMJD'],
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

        return df
