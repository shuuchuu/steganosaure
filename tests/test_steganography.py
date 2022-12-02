import pathlib

import hypothesis
import pytest

from steganosaure.steganography import decrypt, encrypt


@hypothesis.given(
    text=hypothesis.strategies.text(
        hypothesis.strategies.characters(
            blacklist_categories=("Cs",), blacklist_characters=("\x00")
        )
    )
)
def test_encrypt_decrypt_museum(
    text: str,
    museum_image_path: pathlib.Path,
    tmp_path_factory: pytest.TempPathFactory,
) -> None:
    output_image_path = tmp_path_factory.mktemp("encrypted") / "image.png"
    encrypt(text, museum_image_path, output_image_path)
    decrypted = decrypt(output_image_path)
    assert text == decrypted
