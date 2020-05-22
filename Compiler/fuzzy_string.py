"""Operations for strings to be used in fuzzy matching, including accumulating and padding."""

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
        """Initialize a fuzzy string."""
        self.value = value
        #self.accumulated_string = FuzzyString.createFuzzyString(value)
        self.num_chars = num_chars
        if num_chars == None:
            self.num_chars = len(value)

    @staticmethod
    @vectorize
    def createFuzzyString(char_list):
        """
        Create an accumulated fuzzy string with a bit 1 at the end to show that
        it's not not_dummy.
        @param: char_list is an array of sints symbolizing ascii chars.
        """
        accumulated = 1
        for i, char in enumerate(char_list):
            accumulated = accumulated + (char << (constants.ASCII_SIZE * i + 1))
        return accumulated

    @staticmethod
    @vectorize
    def padToLen(char_list, num_chars=constants.STRING_LENGTH):
        str_len = len(char_list)
        padding = num_chars - str_len
        if padding > 0:
            for i in range(padding):
                char_list.append(constants.DUMMY_CHARACTER)
        return char_list

    @staticmethod
    @vectorize
    def getChars(accumulated_string, string_len):
        decomposed = accumulated_string.bit_decompose()
        decomposed_chars = Array(string_len, sint)
        for i in range(string_len):
            char = sint.bit_compose(
                decomposed[
                    constants.ASCII_SIZE * i + 1 : constants.ASCII_SIZE * (i + 1) + 1
                ]
            )
            decomposed_chars[i] = char
        return decomposed_chars

    @staticmethod
    def getShingles(char_list, num_chars, c_param, total_size=constants.STRING_LENGTH):
        # for testing purposes only
        # for now it is a list and assume uniqueness
        shingles = Array(total_size - c_param + 1, sint)
        for i in range(num_chars - c_param + 1):
            shingles[i] = mimc_prf_array(char_list[i : i + c_param], keyInt)
        padding = total_size - num_chars
        if padding > 0:
            for i in range(num_chars - c_param + 1, total_size - c_param + 1):
                shingles[i] = constants.DUMMY_CHARACTER
        return shingles

    @staticmethod
    def multiply_with_const(constant, accumulated_chars):
        return constant * accumulated_chars

    # def multiply_val_with_const(self, constant):
    #     return constant * self.accumulated_string

    def levenstein_distance(self, other, other_len):
        other_chars = FuzzyString.getChars(other, other_len)
        return self._levensteinDistance(other_chars, other_len)

    def _levensteinDistance(self, chars_y, y_len):
        chars_x = self.value
        x_len = self.num_chars
        dynamicProgMatrix = Matrix(x_len + 1, y_len + 1, sint)

        for i in range(x_len + 1):
            for j in range(y_len + 1):
                dynamicProgMatrix[i][j] = constants.ZERO

        for i in range(1, x_len + 1):
            dynamicProgMatrix[i][0] = dynamicProgMatrix[i - 1][
                0
            ] + FuzzyString.not_dummy(chars_x[i - 1])
        for j in range(1, y_len + 1):
            dynamicProgMatrix[0][j] = dynamicProgMatrix[0][
                j - 1
            ] + FuzzyString.not_dummy(chars_y[j - 1])

        for j in range(1, y_len + 1):
            for i in range(1, x_len + 1):
                not_dummy_x = FuzzyString.not_dummy(chars_x[i - 1])
                not_dummy_y = FuzzyString.not_dummy(chars_y[j - 1])
                choice_bit = not_dummy_x * not_dummy_y
                # print_ln("choice_bit = %s", choice_bit.reveal())
                curr_eq = BitonicSort.checkEqualityWithKnownVal(
                    chars_x[i - 1], chars_y[j - 1], constants.ASCII_SIZE
                )
                substitution = 1 - curr_eq
                candidate_val1 = dynamicProgMatrix[i - 1][j] + not_dummy_x
                candidate_val2 = dynamicProgMatrix[i][j - 1] + not_dummy_y
                candidate_val3 = (
                    dynamicProgMatrix[i - 1][j - 1] + substitution * choice_bit
                )
                less12 = candidate_val1 < candidate_val2
                less23 = candidate_val2 < candidate_val3
                less31 = candidate_val3 < candidate_val1

                dynamicProgMatrix[i][j] = (
                    candidate_val1 * less12 * (1 - less31)
                    + candidate_val2 * less23 * (1 - less12)
                    + candidate_val3 * less31 * (1 - less23)
                ) * choice_bit + (1 - choice_bit) * (
                    (1 - not_dummy_y) * dynamicProgMatrix[i][j - 1]
                    + not_dummy_y * dynamicProgMatrix[i - 1][j]
                )

        return dynamicProgMatrix[x_len][y_len]

    @staticmethod
    @vectorize
    def not_dummy(character):
        return 1 - BitonicSort.checkEqualityWithKnownVal(
            constants.DUMMY_CHARACTER, character, 10
        )

    @staticmethod
    @vectorize
    def print_accumulated_str(accumulated, string_len=constants.STRING_LENGTH):
        chars = FuzzyString.getChars(accumulated, string_len)
        for i, char in enumerate(chars):
            print_ln("char %s = %s", i, char.reveal())
