#!python3
import math
import sys
import unittest

sys.path.insert(0, '../area_under_curve/')

import area_under_curve as auc


class BoundsTest(unittest.TestCase):
    """Test class for Bounds class"""
    def test_ok(self):
        """run test method"""
        bounds_ok = auc.Bounds(2, 4, .1)
        #print(bounds_ok)
        assert bounds_ok.lower_bound == 2
        assert bounds_ok.upper_bound == 4
        assert bounds_ok.step_size == .1
        assert len(bounds_ok.full_range) == 21
        #print(bounds_ok.full_range)

    @unittest.expectedFailure
    def test_bad_step_size(self):
        """run test method"""
        auc.Bounds(2, 4, 0)

    @unittest.expectedFailure
    def test_bad_bounds(self):
        """run test method"""
        auc.Bounds(2, 2, 1)


class PolynomialTest(unittest.TestCase):
    """Test class for Bounds class"""
    def test_int_ok(self):
        """Correctly evaluate valid polynomial"""
        polynomial_ok = auc.Polynomial({2:3, 1:4, 0:5})
        assert polynomial_ok.evaluate(-2) == 9
        assert polynomial_ok.evaluate(0) == 5
        assert polynomial_ok.evaluate(2) == 25

    def test_frac_ok(self):
        """Correctly evaluate valid polynomial"""
        polynomial_ok = auc.Polynomial({1.5:1})
        assert polynomial_ok.evaluate(0) == 0
        assert polynomial_ok.evaluate(2) == 2 * math.sqrt(2)

    @unittest.expectedFailure
    def test_fraction_reject(self):
        """Don't evaluate negative input with fractional exponents"""
        polynomial_reject_fraction = auc.Polynomial({2.5, 1})
        polynomial_reject_fraction.evaluate(-2)

    @unittest.expectedFailure
    def test_negative_exp_reject(self):
        """Don't support negative exponents"""
        auc.Polynomial({-2, 1})

    @unittest.expectedFailure
    def test_negative_exp_frac_reject(self):
        """Don't support negative exponents"""
        auc.Polynomial({-2.5, 1})


class ParseArgumentsTest(unittest.TestCase):
    """Test class for parsing command line arguments """
    def test_ok(self):
        parsed_params = auc.parse_arguments(["-p", "{3:2}", "-s", ".2", "-a", "simpson", "-l", "-2", "-u", "1.5"])
        assert parsed_params.bounds.step_size == .2
        assert parsed_params.bounds.lower_bound == -2
        assert parsed_params.bounds.upper_bound == 1.5
        assert parsed_params.polynomial.coefficient_dict[3] == 2
        assert parsed_params.algorithm.__name__ == "simpson"

    def test_invalid_algorithm(self):
        parsed_params = auc.parse_arguments(["-p", "{3:2}", "-s", ".2", "-a", "simpsonx"])
        assert parsed_params == None

    def test_negative_exponent(self):
        parsed_params = auc.parse_arguments(["-p", "{-3:2}", "-s", ".2", "-a", "simpson"])
        assert parsed_params == None

    def test_fractional_exponent_negative_value(self):
        parsed_params = auc.parse_arguments(["-p", "{1.5:2}", "-s", ".2", "-l", "-5", "-a", "simpson"])
        assert parsed_params == None

    def test_invalid_step(self):
        parsed_params = auc.parse_arguments(["-p", "{1.5:2}", "-s", "-1"])
        assert parsed_params == None

    def test_invalid_polynomial_set(self):
        parsed_params = auc.parse_arguments(["-p", "{3-1}", "-s", ".2", "-a", "simpson"])
        assert parsed_params == None

    def test_invalid_polynomial_numeric_s(self):
        parsed_params = auc.parse_arguments(["-p", "{3a:2}"])
        assert parsed_params == None

    def test_invalid_polynomial_numeric_v(self):
        parsed_params = auc.parse_arguments(["-p", "{3:2a}"])
        assert parsed_params == None

    def test_invalid_option(self):
        parsed_params = auc.parse_arguments(["-z", "3"])
        assert parsed_params == None     

if __name__ == "__main__":
    unittest.main()