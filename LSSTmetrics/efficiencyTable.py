"""
read the efficiency Table provided by R. Kessler

"""
import numpy as np
from cStringIO import StringIO
import pandas as pd

__all__ = ['EfficiencyTable']


class EfficiencyTable(object):

    def __init__(self, efficiencyTable):

        self.efficiencyTable = efficiencyTable
        self.filterList = efficiencyTable.band.unique().astype('str')

    def effSNR(self, band, SNRvalues):
        """

        Parameters
        ---------

        Returns
        -------
        """

        if band == 'u':
            band = 'g'
        if band == 'y':
            band = 'z'

        return self.interpolatedEfficiency[band](SNRvalues)
 
    

    @property
    def CompactEfficiencyTable(self):
        return pd.pivot_table(self.efficiencyTable, columns='band',
                              values='Eff', index='SNR')

    @classmethod
    def fromDES_EfficiencyFile(cls, fname):
        df = cls.readDES_efficiencyTable(fname)
        return cls(efficiencyTable=df)

    @property
    def interpolatedEfficiency(self):
        from scipy.interpolate import interp1d
        _ = self.CompactEfficiencyTable
        _snr = _.index.values
        effSNR = dict((band, interp1d(_snr, _[band].values))\
                      for band in self.filterList)
        return effSNR


    @staticmethod
    def readDES_efficiencyTable(fname):
        """
        io utility function to return a pandas DataFrame with the SNR and
        efficiency values in each band from DES efficiency Table file provided
        by R. Kessler


        Parameters
        ----------
        fname : string, mandatory
            filename containing the efficiency table


        Returns 
        -------
        a `~pandas.DataFrame` with metadata containing the comments in the file 
        with columns ['SNR', 'Eff', 'band']


        .. notes : A pivoted form can be constructed
        """
        frames = []
        # Dump file to a string
        with open(fname, 'r') as f:
            _ = f.read()

        # Split on occurances of 'FILTER' that gives different band values
        filts = _.split('FILTER')

        # store comments
        metadata = filts[0]

        # Each block is a table for an individual filter
        for i, block in enumerate(filts[1:]):
            # get name of filter
            bandname = block.split('\n')[0][-1]
        # store table in DataFrame
            effstring = 'Eff'
            s = "\n".join(block.split('\n')[1:])
            df = pd.read_table(StringIO(s),
                               lineterminator='\n',
                               delim_whitespace=True,
                               names=['_', 'SNR', effstring])
            del df['_']
            df['band'] = bandname
            frames.append(df)
        df = pd.concat(frames, axis=0, ignore_index=True)
        return df
