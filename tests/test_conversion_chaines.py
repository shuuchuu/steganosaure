import hypothesis
import hypothesis.strategies
import numpy

from steganosaure.conversion_chaines import decode_bits, encode_chaine


def test_encode_chaine_vide() -> None:
    numpy.testing.assert_array_equal(encode_chaine(""), numpy.array([], dtype="uint8"))


def test_decode_bits_vides() -> None:
    numpy.testing.assert_array_equal("", decode_bits(numpy.array([], dtype="uint8")))


def test_encode_chaine() -> None:
    numpy.testing.assert_array_equal(
        encode_chaine("AB"),
        numpy.array([0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0], dtype="uint8"),
    )


def test_decode_bits() -> None:
    assert (
        decode_bits(
            numpy.array([0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0], dtype="uint8")
        )
        == "AB"
    )


@hypothesis.given(
    hypothesis.strategies.text(
        hypothesis.strategies.characters(
            exclude_categories=["Cs"], exclude_characters=["\x00"]
        )
    )
)
def test_encode_decode(texte: str) -> None:
    assert texte == decode_bits(encode_chaine(texte))
