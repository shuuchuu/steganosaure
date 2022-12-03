import numpy

from steganosaure.array_reshaping import pad_array


def test_pad_array() -> None:
    numpy.testing.assert_array_equal(
        pad_array(numpy.array([1, 1, 0]), numpy.arange(10)),
        numpy.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
    )
