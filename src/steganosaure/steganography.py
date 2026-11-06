"""Top-level functions of the steganosaure tool to encrypt and decrypt messages."""

import pathlib

import deal

from .array_reshaping import flatten_array, pad_array, reshape_array
from .bits_manipulation import (
    modify_least_significant_bits,
    retrieve_least_significant_bits,
)
from .image_io import load_image, save_image
from .string_conversion import decode_bits, encode_string


@deal.raises(ValueError, FileNotFoundError)
def encrypt(
    message: str, input_image_path: pathlib.Path, output_image_path: pathlib.Path
) -> None:
    """Encrypt a message in an image.

    If the message doesn't fit in the image, pad_array raises a ValueError.

    Args:
        message: Message to be encrypted.
        input_image_path: Image that will be used to hide the message.
        output_image_path: Resulting image where the message will be hidden.
    """
    input_image = load_image(input_image_path)
    message_array = encode_string(message)
    flat_image = flatten_array(input_image)
    padded_array = pad_array(message_array, flat_image)
    new_image = modify_least_significant_bits(padded_array, flat_image)
    output_image = reshape_array(new_image, input_image.shape)
    save_image(output_image, output_image_path)


def decrypt(image_path: pathlib.Path) -> str:
    """Decrypt a message in an image (at least, try to).

    Args:
        image_path: Image to decrypt.

    Returns:
        The decrypted string.
    """
    image = load_image(image_path)
    flat_image = flatten_array(image)
    bits = retrieve_least_significant_bits(flat_image)
    return decode_bits(bits)
