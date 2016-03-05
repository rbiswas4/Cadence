from distutils.core import setup

setup(# package information
      name="gedankenLSST",
      version="0.0.1dev",
      description='A package to generate LSST light curves without using OpSim',
      long_description='''We can generate LSST light curves using  ''',
      # What code to include as packages
      packages=['gedankenLSST'],
      package_dir={'gedankenLSST':'gedankenLSST'},
      # What data to include as packages
      include_package_data=True,
      package_data={'gedankenLSST': ['example_data/*.FITS',
                                     'example_data/*.dat',
                                      'example_data/*.md']}
      )



setup(# package information
      name="LSSTmetrics",
      version="0.0.1dev",
      description='A package to generate LSST light curves without using OpSim',
      long_description='''We can generate LSST light curves using  ''',
      # What code to include as packages
      packages=['LSSTmetrics'],
      package_dir={'LSSTmetrics':'LSSTmetrics'},
      # What data to include as packages
      include_package_data=True,
      package_data={'LSSTmetrics': ['example_data/*.FITS',
                                     'example_data/*.dat',
                                      'example_data/*.md']}
      )
