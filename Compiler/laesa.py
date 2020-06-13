# Python modules in here can be imported from .mpc files

from Compiler.util import *
from Compiler.types import *
from Compiler.library import *
from Compiler.program import Tape
import Compiler.constants as constants
from Compiler.bitonic_sort import BitonicSort
from Compiler.fuzzy_string import FuzzyString

class laesaDataSet(object):
    def __init__(self, num_pivots=constants.NUM_PIVOTS, num_chars=constants.STRING_LENGTH, threshold=constants.THRESHOLD, data=None, matrix=None):
        self.num_pivots = num_pivots
        self.num_chars = num_chars
        self.threshold = threshold
        self.num_shingles = num_chars - c_param + 1
        self.t = (constants.TWO * cint(c_param) - constants.ONE) * threshold
        if (matrix != None) and (data != None):
            self.data = data
            self.matrix = matrix
        elif data != None:
            self.data = list(map(lambda x: FuzzyString.createFuzzyString(FuzzyString.padToLen(x, num_chars)), data))
            # For now leaking len of word, later replace len(x) with a sint which is input with data and put dummy shingles
            self.shingledData = list(map(lambda x: FuzzyString.getShingles(x, len(x), c_param, num_chars), data))
        else:
            self.data = []
            self.shingledData = []

    def checkFuzzyMatch(self, fuzzyMatchStr, shingles):
        ## t can be pre-set
        potentialMatches = []
        for i, point in enumerate(self.shingledData):
            shingles_dist = cShinglesDataSet.shinglesDist(shingles, point, self.num_shingles)
            potentialMatches.append(FuzzyString.multiply_with_const(shingles_dist.less_than(self.t, constants.MAX_SHINGLES_DIST_BITS), self.data[i]))
        BitonicSort.pushZerosToBack(potentialMatches)

        candidates = potentialMatches[:constants.NUMBER_OF_CANDIDATES]
        match = []

        for i, candidate in enumerate(candidates):
            dist_val = fuzzyMatchStr.levenstein_distance(candidate, self.num_chars)
            match.append(dist_val.less_than(self.threshold, constants.MAX_DIST_BITS))

        BitonicSort.pushZerosToBack(match)
        return match[0]

    @staticmethod
    @vectorize
    def shinglesDist(shingles1, shingles2, num_shingles):
        dist = (num_shingles + num_shingles)
        for s in shingles1:
            for t in shingles2:
                # equality = BitonicSort.checkEqualityWithKnownVal(s, t, 64)
                #equality = BitonicSort.checkEqualityWithKnownVal(s, t, constants.SHINGLE_COMP_SIZE)
                equality = t.equal(s, bit_length=16)
                dist -= (equality + equality)
        return dist

    def printData(self):
        for d in self.data:
            dlist = list(map(lambda x: x.reveal(), FuzzyString.getChars(d, constants.STRING_LENGTH)))
            print_ln("%s", dlist)