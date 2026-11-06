import pathlib

import hypothesis
import hypothesis.extra.numpy
import hypothesis.strategies
import numpy
import pytest

from steganosaure.images import charge_image, sauvegarde_image


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
def test_sauvegarde_charge(
    image: numpy.ndarray,
    tmp_path_factory: pytest.TempPathFactory,
) -> None:
    chemin_relue = tmp_path_factory.mktemp("images") / "relue.png"
    sauvegarde_image(image, chemin_relue)
    relue = charge_image(chemin_relue)
    numpy.testing.assert_array_equal(image, relue)


@pytest.mark.parametrize(
    "fixture_chemin_image", ["chemin_image_musee", "chemin_image_taille"]
)
def test_charge_sauvegarde_charge(
    fixture_chemin_image: str,
    request: pytest.FixtureRequest,
    tmp_path: pathlib.Path,
) -> None:
    image = charge_image(request.getfixturevalue(fixture_chemin_image))
    chemin_relue = tmp_path / "relue.png"
    sauvegarde_image(image, chemin_relue)
    relue = charge_image(chemin_relue)
    numpy.testing.assert_array_equal(image, relue)
