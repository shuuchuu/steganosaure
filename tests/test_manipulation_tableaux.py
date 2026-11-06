import numpy
import pytest

from steganosaure.manipulation_tableaux import complete_tableau


def test_complete_tableau() -> None:
    numpy.testing.assert_array_equal(
        complete_tableau(numpy.array([1, 1, 0]), numpy.arange(10)),
        numpy.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
    )


def test_complete_tableau_trop_grand() -> None:
    with pytest.raises(ValueError, match="10 > 3"):
        complete_tableau(numpy.arange(10), numpy.array([1, 1, 0]))
