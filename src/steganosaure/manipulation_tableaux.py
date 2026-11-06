"""Manipulation de tableaux numpy."""

import deal
import numpy


def aplatit_tableau(tableau: numpy.ndarray) -> numpy.ndarray:
    """Aplatit le tableau donné pour qu'il n'ait qu'une dimension.

    Args:
        tableau: Tableau numpy à aplatir.

    Returns:
        Tableau plat.
    """
    return tableau.flatten()


def reforme_tableau(
    tableau_plat: numpy.ndarray, forme: tuple[int, ...]
) -> numpy.ndarray:
    """Rend à un tableau sa forme d'origine.

    Args:
        tableau_plat: Tableau numpy plat.
        forme: Forme à rendre.

    Returns:
        Le tableau remis en forme.
    """
    return tableau_plat.reshape(forme)


@deal.raises(ValueError)
def complete_tableau(
    petit_tableau: numpy.ndarray, grand_tableau: numpy.ndarray
) -> numpy.ndarray:
    """Complète le petit tableau par des 0 jusqu'à la taille du grand tableau.

    Args:
        petit_tableau: Tableau numpy de nombres.
        grand_tableau: Tableau numpy.

    Returns:
        Un tableau numpy de même dtype et de mêmes premiers éléments que petit_tableau,
        de la taille de grand_tableau.

    Raises:
        ValueError: Si petit_tableau est plus grand que grand_tableau (le message ne
            tient pas dans l'image).
    """
    if petit_tableau.size > grand_tableau.size:
        msg = (
            "Le tableau à compléter est plus grand que le tableau de référence : "
            f"{petit_tableau.size} > {grand_tableau.size}"
        )
        raise ValueError(msg)
    return numpy.pad(petit_tableau, (0, grand_tableau.size - petit_tableau.size))
