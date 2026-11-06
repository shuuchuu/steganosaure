"""Manipulation de bits."""

import numpy

from steganosaure.manipulation_bits import (
    extrait_bits_poids_faible,
    modifie_bits_poids_faible,
)


def test_extrait_bits_poids_faible() -> None:
    numpy.testing.assert_array_equal(
        extrait_bits_poids_faible(numpy.array([1, 3, 2])), numpy.array([1, 1, 0])
    )


def test_modifie_bits_poids_faible() -> None:
    numpy.testing.assert_array_equal(
        modifie_bits_poids_faible(numpy.array([1, 1, 0]), numpy.array([1, 2, 3])),
        numpy.array([1, 3, 2]),
    )
