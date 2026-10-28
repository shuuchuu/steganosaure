import pathlib

import hypothesis
import hypothesis.extra.numpy
import hypothesis.strategies
import numpy
import pytest

from steganosaure.image_io import load_image, save_image


@hypothesis.settings(deadline=2000)
@hypothesis.given(
    image=hypothesis.extra.numpy.arrays(
        dtype="uint8",
        shape=hypothesis.strategies.tuples(
            hypothesis.strategies.integers(min_value=16, max_value=1024),
            hypothesis.strategies.integers(min_value=16, max_value=1024),
            hypothesis.strategies.just(3),
        ),
        elements=hypothesis.strategies.integers(min_value=0, max_value=255),
    )
)
def test_save_load(
    image: numpy.ndarray,
    tmp_path_factory: pytest.TempPathFactory,
) -> None:
    saved_and_loaded_path = tmp_path_factory.mktemp("images") / "saved_and_loaded.png"
    save_image(image, saved_and_loaded_path)
    saved_and_loaded = load_image(saved_and_loaded_path)
    numpy.testing.assert_array_equal(image, saved_and_loaded)


@pytest.mark.parametrize("image_path_fixture", ["museum_image_path", "size_image_path"])
def test_load_save_load(
    image_path_fixture: str,
    request: pytest.FixtureRequest,
    tmp_path: pathlib.Path,
) -> None:
    image = load_image(request.getfixturevalue(image_path_fixture))
    saved_and_loaded_path = tmp_path / "saved_and_loaded.png"
    save_image(image, saved_and_loaded_path)
    saved_and_loaded = load_image(saved_and_loaded_path)
    numpy.testing.assert_array_equal(image, saved_and_loaded)
