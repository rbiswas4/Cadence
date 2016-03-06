#!/usr/bin/env python


from efficiencyTable import EfficiencyTable
et = EfficiencyTable.fromDES_EfficiencyFile(fname='example_data/SEARCHEFF_PIPELINE_DES.DAT')
print (et.efficiencyTable.head())
ct = et.CompactefficiencyTable
print (ct.head())
x = EfficiencyTable.readDES_efficiencyTable(fname='example_data/SEARCHEFF_PIPELINE_DES.DAT')
print (all(x == et.efficiencyTable))
