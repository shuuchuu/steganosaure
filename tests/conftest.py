import pathlib

import pytest


@pytest.fixture(scope="session")
def dossier_images() -> pathlib.Path:
    return pathlib.Path(__file__).parent / "images"


@pytest.fixture(scope="session")
def chemin_image_musee(dossier_images: pathlib.Path) -> pathlib.Path:
    return dossier_images / "musee.jpg"


@pytest.fixture(scope="session")
def chemin_image_taille(dossier_images: pathlib.Path) -> pathlib.Path:
    return dossier_images / "taille.png"
