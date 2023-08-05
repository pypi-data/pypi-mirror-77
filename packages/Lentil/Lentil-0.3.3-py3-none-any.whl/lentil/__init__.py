from lentil import convolvable
from lentil import detector
from lentil import modeltools
from lentil.plane import *
from lentil.prop import propagate
from lentil import radiometry
from lentil import util
from lentil import wfe
from lentil import zernike

# Enforce Python version during import
# https://docs.python.org/3/library/sys.html#sys.hexversion
import sys
if sys.hexversion < 0x030600F0:
    raise ImportError('Lentil requires Python >= 3.6')

__version__ = '0.3.3'
