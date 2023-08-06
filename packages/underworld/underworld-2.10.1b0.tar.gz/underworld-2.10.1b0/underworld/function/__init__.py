##~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~##
##                                                                                   ##
##  This file forms part of the Underworld geophysics modelling application.         ##
##                                                                                   ##
##  For full license and copyright information, please refer to the LICENSE.md file  ##
##  located at the project root, or contact the authors.                             ##
##                                                                                   ##
##~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~##

"""
The function module contains the Function class, and related classes.

Function objects are constructed in python, but evaluated in C for 
efficiency. They provide a high level interface for users to compose model
behaviour (such as viscosity), as well as a natural interface by which
discrete data (such as meshvariables) may be utilised.

"""

from ._function import Function, FunctionInput, input, coord
from . import math
from . import analytic
from . import misc
from . import tensor
from . import exception
from . import view
from . import shape
from . import branching
from . import rheology
