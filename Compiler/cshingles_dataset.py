# Python modules in here can be imported from .mpc files

from Compiler.util import *
from Compiler.types import *
from Compiler.library import *
from Compiler.program import Tape
import Compiler.constants as constants
from Compiler.bitonic_sort import BitonicSort
from Compiler.fuzzy_string import FuzzyString

class cShinglesDataSet(object):
    def __init__(self, c_param=2, num_chars=5, threshold=constants.TWO, max_levenstein=15, data=None):
        self.c_param = c_param
        self.num_chars = num_chars
        self.threshold = threshold
        self.t = (constants.TWO * cint(c_param) - constants.ONE) * threshold
        self.max_levenstein = max_levenstein
        if data != None:
            self.data = list(map(lambda x: FuzzyString.createFuzzyString(x), data))
            # For now leaking len of word, later replace len(x) with num_chars
            self.shingledData = list(map(lambda x: FuzzyString.getShingles(x, len(x), c_param), data))
        else:
            self.data = []
            self.shingledData = []

    def checkFuzzyMatch(self, fuzzyMatchStr, shingles):
        ## t can be pre-set
        potentialMatches = []
        for i, point in enumerate(self.shingledData):
            shingles_dist = cShinglesDataSet.shinglesDist(shingles, point)
            #print_ln("shingles_dist = %s", shingles_dist.reveal())
            #print_ln("t = %s", self.t.reveal())
            potential = shingles_dist.less_than(self.t)
            #print_ln("potential = %s", potential.reveal())
            potentialMatches.append(FuzzyString.multiply_with_const(potential, self.data[i]))
        BitonicSort.pushZerosToBack(potentialMatches)
        candidates = potentialMatches[:constants.NUMBER_OF_CANDIDATES]
        match = []
        for i, candidate in enumerate(candidates):
            dist_val = fuzzyMatchStr.levenstein_distance(candidate, self.num_chars)
            match.append(self.threshold > dist_val)
        #dataSize = len(potentialMatches)
        BitonicSort.pushZerosToBack(match)
        return match[0]

    @staticmethod
    @vectorize
    def shinglesDist(shingles1, shingles2):
        # TODO change this to support a fixed length for shingles2
        sizeShingles1 = len(shingles1)
        sizeShingles2 = len(shingles2)
        dist = cint(sizeShingles1 + sizeShingles2)
        for s in shingles1:
            for t in shingles2:
                equality = BitonicSort.checkEqualityWithKnownVal(s, t, 10)
                dist -= (equality + equality)
        return dist
