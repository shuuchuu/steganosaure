"""String to bits conversion (and vice versa) utilities."""

import deal
import numpy


def encode_string(string: str) -> numpy.ndarray:
    """
    Convert a string (utf8) into a numpy array of bits.

    Args:
        string: The string to convert.

    Returns:
        Numpy array of dtype uint8 (there is no true boolean type in numpy) that
        contains the utf8 bits (not bytes, so 0s and 1s) representing the input string.
    """
    return numpy.unpackbits(numpy.array(list(string.encode("utf8")), dtype="uint8"))


@deal.raises(UnicodeDecodeError)
def decode_bits(bits: numpy.ndarray) -> str:
    """
    Convert back a  numpy array of bits into a string.

    Args:
        bits: Numpy array of dtype uint8 containing only 0s and 1s representing valid
              utf8.

    Returns:
        The corresponding string.
    """
    return bytes(numpy.packbits(bits)).decode("utf8").rstrip("\x00")
