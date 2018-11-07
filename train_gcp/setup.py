from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = ['pydicom',
                     'keras',
                     'google-cloud-storage',
                     'numpy',
                     'setuptools',
                     'pandas',
                     'argparse',
                     'Pillow',
                     'sklearn'
                     ]

setup(name='z_project',
      version='1.0',
      install_requires=REQUIRED_PACKAGES,
      include_package_data=True,
      packages=find_packages(),
      description='Bla'
)