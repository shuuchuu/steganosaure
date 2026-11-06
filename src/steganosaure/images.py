"""Chargement et sauvegarde d'images."""

import pathlib
import sys

import numpy
import skimage


def charge_image(chemin_image: pathlib.Path) -> numpy.ndarray:
    """Charge une image dans un tableau numpy.

    Args:
        chemin_image: Chemin de l'image à charger.

    Returns:
        Un tableau numpy de dtype uint8, de dimensions (hauteur, largeur, canaux).
    """
    return skimage.util.img_as_ubyte(skimage.io.imread(chemin_image))


def sauvegarde_image(image: numpy.ndarray, chemin_image: pathlib.Path) -> None:
    """Sauvegarde une image.

    Args:
        image: Tableau numpy qui représente l'image à sauvegarder.
        chemin_image: Chemin de l'image de sortie, de préférence un .png : un format
            avec perte comme le .jpg change les bits de poids faible, et perd le
            message caché.
    """
    if chemin_image.suffix.lower() != ".png":
        print(
            f"{chemin_image} n'est pas un .png : un format avec perte perd le message",
            file=sys.stderr,
        )
    skimage.io.imsave(chemin_image, image, check_contrast=False)
