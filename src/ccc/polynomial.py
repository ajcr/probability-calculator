from typing import Iterable

from sympy import Poly, Rational, factorial, binomial
from sympy.abc import x


def degrees_to_polynomial(degrees: Iterable[int]) -> Poly:
    """
    For each degree in a set, create the polynomial with those
    terms having coefficient 1 (and all other terms zero), e.g.:

        {0, 2, 5} -> x**5 + x**2 + 1

    """
    degrees_dict = dict.fromkeys(degrees, 1)
    return Poly.from_dict(degrees_dict, x)


def degrees_to_polynomial_with_fractional_coeff(degrees: Iterable[int], n: int, total: int) -> Poly:
    """
    For each degree in a set, create the polynomial with those
    terms with degree d having a rational coefficient (d / n)**n:

        {5} -> (n / total)**5 * x**5 / 5!

    """
    degree_coeff_dict = {}

    for degree in degrees:
        degree_coeff_dict[degree] = Rational(n, total) ** degree / factorial(degree)

    return Poly.from_dict(degree_coeff_dict, x)


def degrees_to_polynomial_with_binomial_coeff(degrees: Iterable[int], n: int) -> Poly:
    """
    For each degree in a set, create the polynomial with those
    terms with degree d having coefficient binomial(n, d):

        {0, 2, 5} -> bin(n, 5)*x**5 + bin(n, 2)*x**2 + 1

    """
    degree_coeff_dict = {}

    for degree in degrees:
        degree_coeff_dict[degree] = binomial(n, degree)

    return Poly.from_dict(degree_coeff_dict, x)


def degrees_to_polynomial_with_factorial_coeff(degrees: Iterable[int]) -> Poly:
    """
    For each degree in a set, create the polynomial with those
    terms with degree d having coefficient 1/n!:

        {0, 2, 5} -> x**5 / 5! + x**2 / 2!  + 1 / 1!

    """
    degree_coeff_dict = {}

    for degree in degrees:
        degree_coeff_dict[degree] = 1 / factorial(degree)

    return Poly.from_dict(degree_coeff_dict, x)
