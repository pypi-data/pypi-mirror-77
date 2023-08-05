
# -------------------------------------------------------- #
''' Import High Level Libs '''
# -------------------------------------------------------- #
import os,shutil
import glob
import tarfile,sys
import time
import subprocess
import re
import inspect
import pickle
import numpy
import string
import random
import h5py
import copy
# -------------------------------------------------------- #

# -------------------------------------------------------- #
''' Import Low Level Libs '''
# -------------------------------------------------------- #

# list all py files within this directory
from os.path import dirname, basename, isdir, realpath
modules = list( basename(f)[:-3] for f in glob.glob(dirname(__file__)+"/*.py") if not ('__init__.py' in f) )

# Dynamically import all modules within this folder (namespace preserving)
for module in modules:
    exec('from .%s import *' % module)

# Cleanup
del modules, module

# Setup plotting backend
alert('Applying custom matplotlib settings.','positive')
from matplotlib import rc
rc('font', **{'family': 'serif'})
# rc('text', usetex=True)
import matplotlib as mpl
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['mathtext.rm'] = 'serif'
mpl.rcParams['lines.linewidth'] = 0.8
mpl.rcParams['font.size'] = 18
mpl.rcParams['axes.labelsize'] = 24
mpl.rcParams['axes.titlesize'] = 24
mpl.rcParams['xtick.labelsize'] = 18
mpl.rcParams['ytick.labelsize'] = 18
mpl.rcParams['legend.frameon'] = False
mpl.rcParams['legend.fontsize'] = 18
# Use classic MPL lines and dashes by default
if 'lines.dashed_pattern' in mpl.rcParams: mpl.rcParams['lines.dashed_pattern'] = [5, 2]
if 'lines.dashdot_pattern' in mpl.rcParams: mpl.rcParams['lines.dashdot_pattern'] = [3, 5, 1, 5]
if 'lines.dotted_pattern' in mpl.rcParams: mpl.rcParams['lines.dotted_pattern'] = [1, 3]
#
del mpl,rc
