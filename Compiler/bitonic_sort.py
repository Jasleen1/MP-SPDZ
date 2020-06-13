from Compiler.util import *
from Compiler.types import *
from Compiler.library import *
from Compiler.program import Tape
import Compiler.constants as constants
from Compiler.permutation import *


class BitonicSort(object):
    @staticmethod
    def compareAndSwap(a, b, comp):
        pred = comp(a, b)
        add_to_a = pred * (b - a) 
        add_to_b = - add_to_a
        return add_to_a + a, add_to_b + b

    @staticmethod
    @vectorize
    def greaterIfZero(a, b):
        greater = a.equal(constants.ZERO, bit_length=1)#BitonicSort.checkEqualityWithKnownVal(constants.ZERO, a, 1)
        return (1 - greater)

    @staticmethod
    @vectorize
    def checkEqualityWithKnownVal(x: cint, y, size):
        # x_bits = x.bit_decompose()
        y_bits = bit_decompose(y, size+1)
        x_bits = bit_decompose(x, size+1)
        equals = constants.ONE
        #mul_array = Array(size, sbit)
        for i in range(size):
            bit_mult = x_bits[i] * y_bits[i]
            curr_eq = (constants.ONE - (x_bits[i] + y_bits[i] - (bit_mult + bit_mult)))
            #print_ln("bit number = %s, x_bit = %s, y_bit = %s", i, x_bits[i].reveal(), y_bits[i].reveal())
            #print_ln("Biteq %s = %s", i, curr_eq.reveal())
            equals = curr_eq * equals
        return equals

    @staticmethod
    @vectorize
    def pushZerosToBack(sint_list):
        sort(sint_list, BitonicSort.greaterIfZero)
