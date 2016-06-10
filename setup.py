from distutils.core import setup
import sys
import os
import re


versionRegExp = re.compile("__version__ = \"(.*?)\"")

gLSST = "gedankenLSST"
gpackageDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), gLSST)
gvFile = os.path.join(gLSST, 'version.py')

metrics_pname = "LSSTmetrics"
gpackageDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), metrics_pname)
metric_vFile = os.path.join(metrics_pname, 'version.py')

with open(metric_vFile, 'r') as f:
    s = f.read()
metrics_version = versionRegExp.findall(s)[0]

with open(gvFile, 'r') as f:
    s = f.read()
gversion = versionRegExp.findall(s)[0]


setup(# package information
      name=gLSST,
      version=gversion,
      description='A package to generate LSST light curves without using OpSim',
      long_description='''We can generate LSST light curves using  ''',
      # What code to include as packages
      packages=[gLSST],
      package_dir={gLSST:'gedankenLSST'},
      # What data to include as packages
      include_package_data=True,
      package_data={gLSST: ['example_data/*.FITS',
                            'example_data/*.DAT',
                            'example_data/*.dat',
                            'example_data/*.md']}
      )



setup(# package information
      name=metrics_pname,
      version=metrics_version,
      description='A package to generate LSST light curves without using OpSim',
      long_description='''We can generate LSST light curves using  ''',
      # What code to include as packages
      packages=[metrics_pname],
      package_dir={metrics_pname:'LSSTmetrics'},
      # What data to include as packages
      include_package_data=True,
      package_data={metrics_pname: ['example_data/*.FITS',
                                    'example_data/*.dat',
                                    'example_data/*.DAT',
                                    'example_data/*.md']}
      )
