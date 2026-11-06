import pathlib

import pytest


@pytest.fixture(scope="session")
def images_dir() -> pathlib.Path:
    return pathlib.Path(__file__).parent / "images"


@pytest.fixture(scope="session")
def museum_image_path(images_dir: pathlib.Path) -> pathlib.Path:
    return images_dir / "museum.jpg"


@pytest.fixture(scope="session")
def size_image_path(images_dir: pathlib.Path) -> pathlib.Path:
    return images_dir / "size.png"
