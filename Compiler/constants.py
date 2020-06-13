"""Store various constants for cshingles_dataset and associated files."""

from Compiler.types import *

ZERO = cint(0)
ONE = cint(1)
TWO = cint(2)
THREE = cint(3)

DUMMY_CHARACTER = ZERO

STRING_COMP_SIZE = 1

NUMBER_OF_CANDIDATES = 15

ASCII_SIZE = 8

STRING_LENGTH = 30

cSHINGLES = 2

cSHINGLES_LENGTH = (STRING_LENGTH - cSHINGLES + 1)

THRESHOLD = THREE

SHINGLE_COMP_SIZE = ASCII_SIZE * cSHINGLES

MAX_DIST = STRING_LENGTH
MAX_DIST_BITS = 5 # this is = ciel(log(max_dist))
MAX_SHINGLES_DIST_BITS = 6 # this is = ciel(log(2 * shingle_comp_size))

MAX_CANDIDATE_BITS = 3#=log(NUMBER_OF_CANDIDATES)

NUM_PIVOTS = 100 # not used