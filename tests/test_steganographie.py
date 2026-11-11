import pathlib

import hypothesis
import hypothesis.strategies
import pytest

from steganosaure.steganographie import chiffre, dechiffre


@hypothesis.settings(deadline=None)
@hypothesis.given(
    texte=hypothesis.strategies.text(
        hypothesis.strategies.characters(
            exclude_categories=["Cs"],
            exclude_characters=["\x00"],
        )
    )
)
def test_chiffre_dechiffre_musee(
    texte: str,
    chemin_image_musee: pathlib.Path,
    tmp_path_factory: pytest.TempPathFactory,
) -> None:
    chemin_image_sortie = tmp_path_factory.mktemp("chiffrees") / "image.png"
    chiffre(texte, chemin_image_musee, chemin_image_sortie)
    message = dechiffre(chemin_image_sortie)
    assert texte == message
