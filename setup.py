from setuptools import setup
import codecs
import os

def read_readme():
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

setup(
      # Basic information
      name='biosim',
      version='0.05',

      # Packages to include
      packages=['biosim'],

      # Metadata
      description='A simulation of an ecosystem on an isolated island with two species and four environments',
      long_description=read_readme(),
      author='William Tobias Grenersen, Lars Engsæth',
      author_email='wigrener@nmbu.no,laen@nmbu.no',
      keywords='biosimulation',
      classifiers=[
        'Development Status :: 1 - Pre-Alpha',
        'Intended Audience :: Users',
        'Topic :: Science :: Biosimulation',
        'Programming Language :: Python :: 3.8',
        ]
)