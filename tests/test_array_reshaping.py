import numpy
import pytest

from steganosaure.array_reshaping import pad_array


def test_pad_array() -> None:
    numpy.testing.assert_array_equal(
        pad_array(numpy.array([1, 1, 0]), numpy.arange(10)),
        numpy.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
    )


def test_pad_array_too_big() -> None:
    with pytest.raises(ValueError, match="10 > 3"):
        pad_array(numpy.arange(10), numpy.array([1, 1, 0]))
