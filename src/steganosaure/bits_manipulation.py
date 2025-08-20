"""Bits manipulation utilities."""

import numpy


def retrieve_least_significant_bits(array: numpy.ndarray) -> numpy.ndarray:
    """
    Retrieve the least significant bits of all the elements of a numpy array.

    E.g., for the array numpy.array([1, 2, 3]), it should return numpy.array([1, 0, 1]).
    That's because the binary representations of 1, 2 and 3 are 00000001, 00000010 and
    00000011, so if you only keep the last bit, you obtain 1, 0 and 1.

    Args:
        array: Numpy array of numbers (must support the & binary operator).

    Returns:
        A numpy array of the same dtype as the input array, with only the least
        significant bits kept.
    """
    return array & 1


def modify_least_significant_bits(
    message: numpy.ndarray, image: numpy.ndarray
) -> numpy.ndarray:
    """
    Modify the least significant bits of the image array to match the message array.

    E.g., for the arrays:

    - message: numpy.array([1, 1, 0])
    - image: numpy.array([1, 2, 3])

    It should return numpy.array([1, 3, 2]). That's because the binary representations
    of 1, 2 and 3 are 00000001, 00000010 and 00000011, so when we set their last bit to
    respectively 1, 1 and 0, we obtain 00000001, 00000011 and 00000010, ie 1, 3 and 2 in
    decimal form.

    Args:
        message: Numpy array of bits (0s and 1s).
        image: Numpy array of numbers (must support the >>, << and | binary operators).

    Returns:
        A numpy array of the same dtype as the most general input array, with the least
        significant bits of message and all the other bits of image.
    """
    return image >> 1 << 1 | message
