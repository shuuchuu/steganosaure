import pathlib

from steganosaure.cli import create_parser


def test_parse_decrypt() -> None:
    args = create_parser().parse_args(["decrypt", "cache.png"])
    assert args.command == "decrypt"
    assert args.image_path == pathlib.Path("cache.png")


def test_parse_encrypt() -> None:
    args = create_parser().parse_args(["encrypt", "Bonjour", "museum.jpg", "cache.png"])
    assert args.command == "encrypt"
    assert args.message == "Bonjour"
    assert args.input_image_path == pathlib.Path("museum.jpg")
    assert args.output_image_path == pathlib.Path("cache.png")
