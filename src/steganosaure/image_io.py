"""Image loading and saving utilities."""

import pathlib
import sys

import numpy
import skimage


def load_image(image_path: pathlib.Path) -> numpy.ndarray:
    """
    Load an image into a numpy array.

    Args:
        image_path: Path to the image to load.

    Returns:
        A numpy array of dtype uint8 with dimensions (width, height, 3).
    """
    return skimage.util.img_as_ubyte(skimage.io.imread(image_path))


def save_image(image: numpy.ndarray, image_path: pathlib.Path) -> None:
    """
    Save an image.

    Args:
        image: Numpy array representing the image to save.
        image_path: Path of the output image.
    """
    png_path = image_path.with_suffix(".png")
    if image_path.suffix.lower() != ".png":
        print(
            f"Must save image as png: using {png_path} instead of {image_path}",
            file=sys.stderr,
        )
    skimage.io.imsave(image_path, image, plugin="pil", check_contrast=False)
