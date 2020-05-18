from Compiler.util import *
from Compiler.types import *
from Compiler.library import *
from Compiler.program import Tape
import Compiler.constants as constants
from Compiler.bitonic_sort import BitonicSort


keyInt = sint(2)



# MiMC
rounds = 161

@vectorize
def mimc_prf(m, key):
    x = m

    for r in range(rounds):
        x = (x + key + r) ** 3

    x = x + key
    return x

@vectorize
def mimc_prf_array(m_array, key):
    # just for testing purposes
    x = constants.ZERO
    for m in m_array:
        x = x + m
        for r in range(rounds):
            x = (x + key + r) ** 3
        x = x + key
    return x



class FuzzyString(object):
    def __init__(self, value, num_chars=None):
        self.value = value
        self.accumulated_string = FuzzyString.createFuzzyString(value)
        self.num_chars = num_chars
        if num_chars == None:
            self.num_chars = len(value)

    @staticmethod
    @vectorize
    def createFuzzyString(char_list):
        accumulated = 0
        for i, char in enumerate(char_list):
            accumulated = accumulated + (char << (constants.ASCII_SIZE*i))
        return accumulated

    @staticmethod
    @vectorize
    def getChars(accumulated_string, string_len):
        decomposed = accumulated_string.bit_decompose()
        check = (len(decomposed) % constants.ASCII_SIZE == 0)
        decomposed_chars = Array(string_len, sint)
        for i in range(string_len):
            char = sint.bit_compose(decomposed[constants.ASCII_SIZE*i:constants.ASCII_SIZE*(i+1)])
            decomposed_chars[i] = char
        return decomposed_chars

    @staticmethod
    def getShingles(char_list, num_chars, c_param):
        # for testing purposes only
        # for now it is a list and assume uniqueness
        shingles = Array(num_chars-c_param+1, sint)
        for i in range(num_chars - c_param):
            shingles[i] = mimc_prf_array(char_list[i:i+c_param], keyInt)
        return shingles

    @staticmethod
    def multiply_with_const(constant, accumulated_chars):
        return constant * accumulated_chars

    def multiply_val_with_const(self, constant):
        return constant * self.accumulated_string

    def levenstein_distance(self, other, other_len):
        other_chars = FuzzyString.getChars(other, other_len)
        return self._levensteinDistance(other_chars, other_len)


    def _levensteinDistance(self, chars_y, y_len):
        chars_x = self.value
        x_len = self.num_chars
        dynamicProgMatrix = Matrix(x_len + 1, y_len + 1, sint)
       
        for i in range(x_len+1):
            for j in range(y_len+1):
                dynamicProgMatrix[i][j] = constants.ZERO
        X = cint(x_len)
        Y = cint(y_len)
        for i in range(1, x_len + 1):
            dynamicProgMatrix[i][0] = i
        for j in range(1, y_len + 1):
            dynamicProgMatrix[0][j] = j

        for j in range(1, y_len + 1):
            for i in range(1, x_len + 1):
                dummy_x = FuzzyString.dummy(chars_x[i - 1])
                dummy_y = FuzzyString.dummy(chars_y[j - 1])
                choice_bit = dummy_x * dummy_y
                #print_ln("choice_bit = %s", choice_bit.reveal())
                curr_eq = BitonicSort.checkEqualityWithKnownVal(chars_x[i-1], chars_y[j-1], constants.ASCII_SIZE)
                substitution = (1 - curr_eq) * choice_bit
                candidate_val1 = dynamicProgMatrix[i-1][j] + dummy_x
                candidate_val2 = dynamicProgMatrix[i][j-1] + dummy_y
                candidate_val3 = dynamicProgMatrix[i-1][j-1] + substitution
                less12 = (candidate_val1 < candidate_val2) * dummy_x + (1-dummy_x)
                less23 = (candidate_val2 < candidate_val3) * dummy_y + (1-dummy_y)
                less31 = (candidate_val3 < candidate_val1) * choice_bit + (1-choice_bit)
                # print_ln("less12 = %s", less12.reveal())
                # print_ln("less23 = %s", less23.reveal())
                # print_ln("less31 = %s", less31.reveal())
                dynamicProgMatrix[i][j] = candidate_val1 * less12 * (1 - less31) + candidate_val2 * less23 * (1 - less12) + candidate_val3 * less31 * (1 - less23)
                #print_ln("dynamicProgMatrix val = %s", dynamicProgMatrix[i][j].reveal())
        return dynamicProgMatrix[x_len][y_len]

    @staticmethod
    @vectorize
    def dummy(character):
        return (1 - BitonicSort.checkEqualityWithKnownVal(constants.DUMMY_CHARACTER, character, 10))

