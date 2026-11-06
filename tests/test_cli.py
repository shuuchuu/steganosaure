import pathlib

from steganosaure.cli import cree_parseur


def test_analyse_dechiffre() -> None:
    args = cree_parseur().parse_args(["dechiffre", "cache.png"])
    assert args.commande == "dechiffre"
    assert args.chemin_image == pathlib.Path("cache.png")


def test_analyse_chiffre() -> None:
    args = cree_parseur().parse_args(["chiffre", "Bonjour", "musee.jpg", "cache.png"])
    assert args.commande == "chiffre"
    assert args.message == "Bonjour"
    assert args.chemin_image_entree == pathlib.Path("musee.jpg")
    assert args.chemin_image_sortie == pathlib.Path("cache.png")
