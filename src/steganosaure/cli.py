"""Interface en ligne de commande de steganosaure."""

from argparse import ArgumentParser
from pathlib import Path

from .steganographie import chiffre, dechiffre


def cree_parseur() -> ArgumentParser:
    """Construit le parseur de la commande steganosaure et de ses deux sous-commandes.

    Returns:
        Le parseur.
    """
    parseur = ArgumentParser(
        prog="steganosaure", description="Cache des messages dans des images"
    )
    sous_parseurs = parseur.add_subparsers(
        help="Commandes", dest="commande", required=True
    )

    parseur_chiffre = sous_parseurs.add_parser("chiffre")
    parseur_chiffre.add_argument("message")
    parseur_chiffre.add_argument("chemin_image_entree", type=Path)
    parseur_chiffre.add_argument("chemin_image_sortie", type=Path)

    parseur_dechiffre = sous_parseurs.add_parser("dechiffre")
    parseur_dechiffre.add_argument("chemin_image", type=Path)
    return parseur


def main() -> None:
    """Point d'entrée du programme."""
    parseur = cree_parseur()
    args = parseur.parse_args()
    if args.commande == "chiffre":
        chiffre(args.message, args.chemin_image_entree, args.chemin_image_sortie)
    else:
        print(dechiffre(args.chemin_image))
