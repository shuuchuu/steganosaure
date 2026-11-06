"""Manipulation de bits."""

import numpy


def extrait_bits_poids_faible(tableau: numpy.ndarray) -> numpy.ndarray:
    """Extrait les bits de poids faible de tous les éléments d'un tableau numpy.

    Par exemple, pour le tableau numpy.array([1, 2, 3]), elle renvoie
    numpy.array([1, 0, 1]). En effet, 1, 2 et 3 s'écrivent 00000001, 00000010 et
    00000011 en binaire : si on ne garde que le dernier bit, on obtient 1, 0 et 1.

    Args:
        tableau: Tableau numpy de nombres (qui acceptent l'opérateur binaire &).

    Returns:
        Un tableau numpy de même dtype que le tableau d'entrée, où seuls les bits de
        poids faible sont gardés.
    """
    return tableau & 1


def modifie_bits_poids_faible(
    message: numpy.ndarray, image: numpy.ndarray
) -> numpy.ndarray:
    """Modifie les bits de poids faible du tableau image pour y écrire le message.

    Par exemple, pour les tableaux :

    - message : numpy.array([1, 1, 0])
    - image : numpy.array([1, 2, 3])

    Elle renvoie numpy.array([1, 3, 2]). En effet, 1, 2 et 3 s'écrivent 00000001,
    00000010 et 00000011 en binaire : quand on met leur dernier bit à 1, 1 et 0, on
    obtient 00000001, 00000011 et 00000010, soit 1, 3 et 2 en décimal.

    Args:
        message: Tableau numpy de bits (des 0 et des 1).
        image: Tableau numpy de nombres (qui acceptent les opérateurs binaires >>, <<
            et |).

    Returns:
        Un tableau numpy du dtype le plus général des deux tableaux d'entrée, avec les
        bits de message en poids faible et tous les autres bits de image.
    """
    return image >> 1 << 1 | message
