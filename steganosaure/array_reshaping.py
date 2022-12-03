"""Array reshaping utilities."""

import numpy


def flatten_array(array: numpy.ndarray) -> numpy.ndarray:
    """
    Flatten the given array so that it has only one dimension.

    Args:
        array: Numpy array to flatten.

    Returns:
        Flat array.
    """
    return array.flatten()


def reshape_array(flat_array: numpy.ndarray, shape: tuple[int, ...]) -> numpy.ndarray:
    """
    Restore the original shape of an array.

    Args:
        flat_array: Flat numpy array.
        shape: Shape to restore.

    Returns:
        Reshaped array.
    """
    return flat_array.reshape(shape)


def pad_array(small_array: numpy.ndarray, big_array: numpy.ndarray) -> numpy.ndarray:
    """
    Pad the small array with 0s to match the size of the big array.

    Args:
        small_array: Numpy array of numbers.
        big_array: Numpy array.

    Returns:
        A numpy array of the same dtype and starting elements than small_array, with the
        size of big_array.
    """
    return numpy.pad(small_array, (0, big_array.size - small_array.size))
