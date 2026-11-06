"""Image loading and saving utilities."""

import pathlib
import sys

import numpy
import skimage


def load_image(image_path: pathlib.Path) -> numpy.ndarray:
    """Load an image into a numpy array.

    Args:
        image_path: Path to the image to load.

    Returns:
        A numpy array of dtype uint8 with dimensions (height, width, channels).
    """
    return skimage.util.img_as_ubyte(skimage.io.imread(image_path))


def save_image(image: numpy.ndarray, image_path: pathlib.Path) -> None:
    """Save an image.

    Args:
        image: Numpy array representing the image to save.
        image_path: Path of the output image, preferably a .png: a lossy format such as
            .jpg changes the least significant bits, and loses the hidden message.
    """
    if image_path.suffix.lower() != ".png":
        print(
            f"{image_path} is not a .png: a lossy format loses the hidden message",
            file=sys.stderr,
        )
    skimage.io.imsave(image_path, image, check_contrast=False)
