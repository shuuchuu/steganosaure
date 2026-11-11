"""Fonctions principales de l'outil steganosaure : chiffrer et déchiffrer un message."""

import pathlib

import deal

from .conversion_chaines import decode_bits, encode_chaine
from .images import charge_image, sauvegarde_image
from .manipulation_bits import (
    extrait_bits_poids_faible,
    modifie_bits_poids_faible,
)
from .manipulation_tableaux import aplatit_tableau, complete_tableau, reforme_tableau


@deal.raises(ValueError, FileNotFoundError)
def chiffre(
    message: str, chemin_image_entree: pathlib.Path, chemin_image_sortie: pathlib.Path
) -> None:
    """Chiffre un message dans une image.

    Si le message ne tient pas dans l'image, complete_tableau lève une ValueError.

    Args:
        message: Message à chiffrer.
        chemin_image_entree: Image qui servira à cacher le message.
        chemin_image_sortie: Image résultat, où le message sera caché.
    """
    image_entree = charge_image(chemin_image_entree)
    tableau_message = encode_chaine(message)
    image_plate = aplatit_tableau(image_entree)
    tableau_complete = complete_tableau(tableau_message, image_plate)
    nouvelle_image = modifie_bits_poids_faible(tableau_complete, image_plate)
    image_sortie = reforme_tableau(nouvelle_image, image_entree.shape)
    sauvegarde_image(image_sortie, chemin_image_sortie)


def dechiffre(chemin_image: pathlib.Path) -> str:
    """Déchiffre le message d'une image (ou du moins, essaie).

    Args:
        chemin_image: Image à déchiffrer.

    Returns:
        La chaîne déchiffrée.
    """
    image = charge_image(chemin_image)
    image_plate = aplatit_tableau(image)
    bits = extrait_bits_poids_faible(image_plate)
    return decode_bits(bits)
