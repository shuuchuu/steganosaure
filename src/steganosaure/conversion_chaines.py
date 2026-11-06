"""Conversion de chaînes de caractères en bits, et inversement."""

import deal
import numpy


def encode_chaine(chaine: str) -> numpy.ndarray:
    """Convertit une chaîne (utf8) en tableau numpy de bits.

    Args:
        chaine: La chaîne à convertir.

    Returns:
        Tableau numpy de dtype uint8 (numpy n'a pas de vrai type booléen) qui contient
        les bits utf8 (pas les octets, donc des 0 et des 1) de la chaîne d'entrée.
    """
    return numpy.unpackbits(numpy.array(list(chaine.encode("utf8")), dtype="uint8"))


@deal.raises(UnicodeDecodeError)
def decode_bits(bits: numpy.ndarray) -> str:
    """Reconvertit un tableau numpy de bits en chaîne.

    Args:
        bits: Tableau numpy de dtype uint8 qui ne contient que des 0 et des 1
              représentant de l'utf8 valide.

    Returns:
        La chaîne correspondante.
    """
    return bytes(numpy.packbits(bits)).decode("utf8").rstrip("\x00")
