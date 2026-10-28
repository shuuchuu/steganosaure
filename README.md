# Creating a Steganography CLI

*[Version française](https://github.com/shuuchuu/steganosaure/tree/main)*

[Steganography](https://en.wikipedia.org/wiki/Steganography) encompasses techniques for concealing a message. It differs from cryptography, which aims not to hide a message but to render it incomprehensible to anyone without the necessary key.

The method we will implement in this practical work is well-known: it involves [modifying the least significant bit of each pixel in an image](https://en.wikipedia.org/wiki/Steganography#Digital_messages). This modification is not visible to the naked eye (although it can be detected through statistical analysis).

This README is the lab's statement, to do it in a GitHub Codespace or a local clone; it is the same as the [lab's notebook](https://colab.research.google.com/github/shuuchuu/labs/blob/main/cli-hands-on-en.ipynb). The [`solution-en` branch](https://github.com/shuuchuu/steganosaure/tree/solution-en) gives a solution, which each step's *Solution* section repeats. It also uses [`deal`](https://deal.readthedocs.io/), which the statement doesn't ask for: its contracts (`@deal.raises`) declare the exceptions a function may raise (`uv add deal`).

## Work Environment

For the labs, we will use GitHub Codespaces, which provides VSCode instances within containers. The free plan of personal accounts gives 120 core hours per month, that is 60 hours on this lab's 2-core machine, and 15 GB of storage. This is more than sufficient for this practical work.

If you do not have a GitHub account, start by creating one [here](https://github.com/signup).

Open the repository in a Codespace: [this link](https://codespaces.new/shuuchuu/steganosaure/tree/main-en), or, on GitHub, **Code** > **Codespaces** > **Create codespace on main-en**. In a local clone, install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run `uv sync` at the root of the repository.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/shuuchuu/steganosaure/tree/main-en)

The labs repository is a `uv` project: the code goes in `src/steganosaure/` and the tests in `tests/`. It does not declare any dependency yet: in the Codespace's terminal, `uv add numpy scikit-image` adds those this lab needs.

Run the tests from this terminal with `uv run pytest` (`pytest` is already among the repository's development dependencies). The `tests/conftest.py` file provides two pytest fixtures, `museum_image_path` and `size_image_path`, the paths of the images in `tests/images/` that step 2 needs: a test receives them by naming them among its parameters.

## Step 1 ⋅ Functions for Converting Strings to Bits and Vice Versa

First, we will focus on converting strings into bits (and vice versa).

A first function, `encode_string`, will take a string as an argument and return a numpy array of the corresponding bits (in utf8 encoding).

A numpy array is a homogeneous data structure (elements of the same type), which we will use in this practical work as a highly enhanced list.

For example, for the string `"ABC"`, we expect the following output array:

```python
numpy.array([0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1])
```

Indeed, `A` is encoded as `01000001` in utf8, `B` as `01000010`, and `C` as `01000011`. The expected array is simply these bits concatenated.

To code this function, here are some useful functions:
- [`str.encode`](https://docs.python.org/3/library/stdtypes.html#str.encode) which returns a `bytes` object (itself an iterable of bytes represented as integers)
- [`numpy.unpackbits`](https://numpy.org/doc/stable/reference/generated/numpy.unpackbits.html), which you can apply to a numpy array previously created from the bytes represented as integers obtained from the `bytes` object. To create the numpy array, you can use [`numpy.array`](https://numpy.org/doc/stable/reference/generated/numpy.array.html) or [`numpy.fromiter`](https://numpy.org/doc/stable/reference/generated/numpy.fromiter.html) and specify `dtype="uint8"` during the call. This argument will allow you to represent the byte values with the most suitable type.

Here is the expected function signature:

```python
def encode_string(string: str) -> numpy.ndarray: ...
```

The `decode_bits` function will handle the reverse transformation. The functions to use are the inverses of those needed for `encode_string`:
- [`bytes.decode`](https://docs.python.org/3/library/stdtypes.html#bytes.decode) which returns a string
- [`numpy.packbits`](https://numpy.org/doc/stable/reference/generated/numpy.packbits.html)

Here is the expected function signature:

```python
def decode_bits(bits: numpy.ndarray) -> str: ...
```

Instructions:

- Create the file `tests/test_string_conversion.py` and create at least one test case per function, using the given example if necessary. To compare two numpy arrays, you can use the dedicated function [`numpy.testing.assert_array_equal`](https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_array_equal.html).
- Create the file `src/steganosaure/string_conversion.py` and implement these two functions inside so that the tests pass.
- Can you design a test that ensures the two functions are indeed inverses of each other? With [`hypothesis`](https://hypothesis.readthedocs.io/) (`uv add --dev hypothesis`), it can run on generated strings: `@hypothesis.given(hypothesis.strategies.text())`.

<details>
<summary>Solution</summary>

`tests/test_string_conversion.py`:

```python
import hypothesis
import hypothesis.strategies
import numpy

from steganosaure.string_conversion import decode_bits, encode_string


def test_encode_empty_string() -> None:
    numpy.testing.assert_array_equal(encode_string(""), numpy.array([], dtype="uint8"))


def test_decode_empty_bits() -> None:
    numpy.testing.assert_array_equal("", decode_bits(numpy.array([], dtype="uint8")))


def test_encode_string() -> None:
    numpy.testing.assert_array_equal(
        encode_string("AB"),
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
def test_encode_decode(text: str) -> None:
    assert text == decode_bits(encode_string(text))
```

`src/steganosaure/string_conversion.py`:

```python
"""String to bits conversion (and vice versa) utilities."""

import deal
import numpy


def encode_string(string: str) -> numpy.ndarray:
    """Convert a string (utf8) into a numpy array of bits.

    Args:
        string: The string to convert.

    Returns:
        Numpy array of dtype uint8 (there is no true boolean type in numpy) that
        contains the utf8 bits (not bytes, so 0s and 1s) representing the input string.
    """
    return numpy.unpackbits(numpy.array(list(string.encode("utf8")), dtype="uint8"))


@deal.raises(UnicodeDecodeError)
def decode_bits(bits: numpy.ndarray) -> str:
    """Convert back a  numpy array of bits into a string.

    Args:
        bits: Numpy array of dtype uint8 containing only 0s and 1s representing valid
              utf8.

    Returns:
        The corresponding string.
    """
    return bytes(numpy.packbits(bits)).decode("utf8").rstrip("\x00")
```

`decode_bits` already removes step 5's null characters: the generated strings exclude them.

</details>

## Step 2 ⋅ Functions for Loading and Saving Images

Now we are going to code two important functions: one will load an image, and the other will save it.

**Note, for our algorithm to work, an image saved and then reloaded must be identical to the original image.**

The loading function will need to load an image into a numpy array with elements as 8-bit integers (for this, you can use the [`scikit-image`](https://scikit-image.org/) package and specifically the functions [`skimage.io.imread`](https://scikit-image.org/docs/stable/api/skimage.io.html#skimage.io.imread) and [`skimage.util.img_as_ubyte`](https://scikit-image.org/docs/stable/api/skimage.util.html#skimage.util.img_as_ubyte)). Here is the expected signature:

```python
def load_image(image_path: pathlib.Path) -> numpy.ndarray: ...
```

The saving function will need to save a numpy array to the specified path. Note that to ensure the reloaded image is equivalent to the saved image while maintaining good quality, it is preferable to save images in `.png` format. You can use the function [`skimage.io.imsave`](https://scikit-image.org/docs/stable/api/skimage.io.html#skimage.io.imsave). It will be useful to pass it the argument `check_contrast=False`. Here is the expected signature:

```python
def save_image(image: numpy.ndarray, image_path: pathlib.Path) -> None: ...
```

Instructions:

- Create the file `tests/test_image_io.py` and create at least one test case to ensure that the crucial point is respected (an image saved and then loaded is the same as the original image).
- Create the file `src/steganosaure/image_io.py` and implement these two functions inside so that the test(s) pass.

<details>
<summary>Solution</summary>

`tests/test_image_io.py`:

```python
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
```

`src/steganosaure/image_io.py`:

```python
"""Image loading and saving utilities."""

import pathlib
import sys

import numpy
import skimage


def load_image(image_path: pathlib.Path) -> numpy.ndarray:
    """Load an image into a numpy array.

    Args:
        image_path: Path to the image to load.

    Returns:
        A numpy array of dtype uint8 with dimensions (height, width, channels).
    """
    return skimage.util.img_as_ubyte(skimage.io.imread(image_path))


def save_image(image: numpy.ndarray, image_path: pathlib.Path) -> None:
    """Save an image.

    Args:
        image: Numpy array representing the image to save.
        image_path: Path of the output image, preferably a .png: a lossy format such as
            .jpg changes the least significant bits, and loses the hidden message.
    """
    if image_path.suffix.lower() != ".png":
        print(
            f"{image_path} is not a .png: a lossy format loses the hidden message",
            file=sys.stderr,
        )
    skimage.io.imsave(image_path, image, check_contrast=False)
```

</details>

## Step 3 ⋅ Bit Manipulation Functions

We will now implement the core of the algorithm: modifying the least significant bit of each pixel to store a bit of information from the string to be hidden.

A brief reminder on bit manipulation:

```python
0b01 & 0b11 == 0b01  # bitwise AND, result bit is 1 if both bits are 1
0b01 | 0b11 == 0b11  # bitwise OR, result bit is 1 if at least one bit is 1
0b11 >> 1 == 0b01  # right shift, fills with 0s
0b11 << 1 == 0b110  # left shift, fills with 0s
```

These representations are equivalent to their decimal notation:

```python
1 & 3 == 1
1 | 3 == 3
3 >> 1 == 1
3 << 1 == 6
```

To achieve this, we will implement two functions. The first one, `retrieve_least_significant_bits`, will return a numpy array of the same size as its argument but containing only 0s or 1s: the least significant bits of the numbers contained in the argument array.

To write this function, feel free to utilize the fact that you can directly apply an operation on a numpy array (including bitwise operations):

```pycon
>>> 3 & 1
1
>>> 2 & 1
0
>>> numpy.array([3, 2]) & 1
array([1, 0])
```

Here is its expected signature:

```python
def retrieve_least_significant_bits(array: numpy.ndarray) -> numpy.ndarray: ...
```

The second function to implement, `modify_least_significant_bits`, will modify the least significant bits of the `image` so that they match the `message` array. Here is its expected signature:

```python
def modify_least_significant_bits(
    message: numpy.ndarray, image: numpy.ndarray
) -> numpy.ndarray: ...
```

Instructions:

- Create the file `tests/test_bits_manipulation.py` and create at least one test case for each function.
- Create the file `src/steganosaure/bits_manipulation.py` and implement these two functions inside so that the tests pass.

<details>
<summary>Solution</summary>

`tests/test_bits_manipulation.py`:

```python
"""Bits manipulation utilities."""

import numpy

from steganosaure.bits_manipulation import (
    modify_least_significant_bits,
    retrieve_least_significant_bits,
)


def test_retrieve_least_significant_bits() -> None:
    numpy.testing.assert_array_equal(
        retrieve_least_significant_bits(numpy.array([1, 3, 2])), numpy.array([1, 1, 0])
    )


def test_modify_least_significant_bits() -> None:
    numpy.testing.assert_array_equal(
        modify_least_significant_bits(numpy.array([1, 1, 0]), numpy.array([1, 2, 3])),
        numpy.array([1, 3, 2]),
    )
```

`src/steganosaure/bits_manipulation.py`:

```python
"""Bits manipulation utilities."""

import numpy


def retrieve_least_significant_bits(array: numpy.ndarray) -> numpy.ndarray:
    """Retrieve the least significant bits of all the elements of a numpy array.

    E.g., for the array numpy.array([1, 2, 3]), it should return numpy.array([1, 0, 1]).
    That's because the binary representations of 1, 2 and 3 are 00000001, 00000010 and
    00000011, so if you only keep the last bit, you obtain 1, 0 and 1.

    Args:
        array: Numpy array of numbers (must support the & binary operator).

    Returns:
        A numpy array of the same dtype as the input array, with only the least
        significant bits kept.
    """
    return array & 1


def modify_least_significant_bits(
    message: numpy.ndarray, image: numpy.ndarray
) -> numpy.ndarray:
    """Modify the least significant bits of the image array to match the message array.

    E.g., for the arrays:

    - message: numpy.array([1, 1, 0])
    - image: numpy.array([1, 2, 3])

    It should return numpy.array([1, 3, 2]). That's because the binary representations
    of 1, 2 and 3 are 00000001, 00000010 and 00000011, so when we set their last bit to
    respectively 1, 1 and 0, we obtain 00000001, 00000011 and 00000010, ie 1, 3 and 2 in
    decimal form.

    Args:
        message: Numpy array of bits (0s and 1s).
        image: Numpy array of numbers (must support the >>, << and | binary operators).

    Returns:
        A numpy array of the same dtype as the most general input array, with the least
        significant bits of message and all the other bits of image.
    """
    return image >> 1 << 1 | message
```

</details>

## Step 4 ⋅ Functions to Manipulate numpy Arrays

The next function, `pad_array`, preprocesses the arguments of `modify_least_significant_bits` so that they are of the same size. It returns `small_array` (which will be our message to hide) padded with zeros up to the size of `big_array` (which will be the image where the message is concealed). You can use [`numpy.pad`](https://numpy.org/doc/stable/reference/generated/numpy.pad.html) for the implementation.

If `small_array` is bigger than `big_array`, the message does not fit in the image: `pad_array` must then raise a `ValueError` whose message gives both sizes.

Here is its expected signature:

```python
def pad_array(
    small_array: numpy.ndarray, big_array: numpy.ndarray
) -> numpy.ndarray: ...
```

Instructions:

- Create the file `tests/test_array_reshaping.py` and write at least one test case for the zero padding, and one that checks the `ValueError` with [`pytest.raises`](https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions).
- Create the file `src/steganosaure/array_reshaping.py` and implement this function inside so that the tests pass.

<details>
<summary>Solution</summary>

`tests/test_array_reshaping.py`:

```python
import numpy
import pytest

from steganosaure.array_reshaping import pad_array


def test_pad_array() -> None:
    numpy.testing.assert_array_equal(
        pad_array(numpy.array([1, 1, 0]), numpy.arange(10)),
        numpy.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
    )


def test_pad_array_too_big() -> None:
    with pytest.raises(ValueError, match="10 > 3"):
        pad_array(numpy.arange(10), numpy.array([1, 1, 0]))
```

`src/steganosaure/array_reshaping.py`:

```python
"""Array reshaping utilities."""

import deal
import numpy


@deal.raises(ValueError)
def pad_array(small_array: numpy.ndarray, big_array: numpy.ndarray) -> numpy.ndarray:
    """Pad the small array with 0s to match the size of the big array.

    Args:
        small_array: Numpy array of numbers.
        big_array: Numpy array.

    Returns:
        A numpy array of the same dtype and starting elements than small_array, with the
        size of big_array.

    Raises:
        ValueError: If small_array is bigger than big_array (the message doesn't fit in
            the image).
    """
    if small_array.size > big_array.size:
        msg = (
            "The array to pad is bigger than the array to match: "
            f"{small_array.size} > {big_array.size}"
        )
        raise ValueError(msg)
    return numpy.pad(small_array, (0, big_array.size - small_array.size))
```

</details>

## Step 5 ⋅ Implementation of Steganography

We have now completed the preparatory phase and have all the necessary functions to implement steganography.

The first function of our tool, `encrypt`, will allow the user to hide a message within an image. Before applying the already developed methods, it will be necessary to use [`numpy.reshape`](https://numpy.org/doc/stable/reference/generated/numpy.reshape.html) to obtain all pixel values in a one-dimensional array, then to give the modified image its original shape back. You can put these two operations in `array_reshaping.py` (`flatten_array`, `reshape_array`).

Here is its expected signature:

```python
def encrypt(
    message: str, input_image_path: pathlib.Path, output_image_path: pathlib.Path
) -> None: ...
```

The second function of our tool, `decrypt`, will allow the user to retrieve the previously hidden message from an image. Here is its expected signature:

```python
def decrypt(image_path: pathlib.Path) -> str: ...
```

The image holds the message followed by the zeros `pad_array` added: decoded, they give null characters (`"\x00"`) at the end of the string. Remove them (`str.rstrip("\x00")`), in `decrypt` or in `decode_bits`; in the latter case, exclude this character from the strings generated in step 1: `hypothesis.strategies.text(hypothesis.strategies.characters(exclude_categories=["Cs"], exclude_characters="\x00"))`. Surrogates (category `Cs`), which `text()` excludes on its own, don't encode to utf8: a `characters` without `exclude_categories` generates them.

Instructions:

- Create the file `tests/test_steganography.py` and write at least one test case to verify the correct functioning of both functions together.
- Create the file `src/steganosaure/steganography.py` and implement these two functions inside to ensure the tests pass.

<details>
<summary>Solution</summary>

`src/steganosaure/array_reshaping.py`, after the imports:

```python
def flatten_array(array: numpy.ndarray) -> numpy.ndarray:
    """Flatten the given array so that it has only one dimension.

    Args:
        array: Numpy array to flatten.

    Returns:
        Flat array.
    """
    return array.flatten()


def reshape_array(flat_array: numpy.ndarray, shape: tuple[int, ...]) -> numpy.ndarray:
    """Restore the original shape of an array.

    Args:
        flat_array: Flat numpy array.
        shape: Shape to restore.

    Returns:
        Reshaped array.
    """
    return flat_array.reshape(shape)
```

`tests/test_steganography.py`:

```python
import pathlib

import hypothesis
import hypothesis.strategies
import pytest

from steganosaure.steganography import decrypt, encrypt


@hypothesis.given(
    text=hypothesis.strategies.text(
        hypothesis.strategies.characters(
            exclude_categories=["Cs"],
            exclude_characters=["\x00"],
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
```

`src/steganosaure/steganography.py`:

```python
"""Top-level functions of the steganosaure tool to encrypt and decrypt messages."""

import pathlib

import deal

from .array_reshaping import flatten_array, pad_array, reshape_array
from .bits_manipulation import (
    modify_least_significant_bits,
    retrieve_least_significant_bits,
)
from .image_io import load_image, save_image
from .string_conversion import decode_bits, encode_string


@deal.raises(ValueError, FileNotFoundError)
def encrypt(
    message: str, input_image_path: pathlib.Path, output_image_path: pathlib.Path
) -> None:
    """Encrypt a message in an image.

    If the message doesn't fit in the image, pad_array raises a ValueError.

    Args:
        message: Message to be encrypted.
        input_image_path: Image that will be used to hide the message.
        output_image_path: Resulting image where the message will be hidden.
    """
    input_image = load_image(input_image_path)
    message_array = encode_string(message)
    flat_image = flatten_array(input_image)
    padded_array = pad_array(message_array, flat_image)
    new_image = modify_least_significant_bits(padded_array, flat_image)
    output_image = reshape_array(new_image, input_image.shape)
    save_image(output_image, output_image_path)


def decrypt(image_path: pathlib.Path) -> str:
    """Decrypt a message in an image (at least, try to).

    Args:
        image_path: Image to decrypt.

    Returns:
        The decrypted string.
    """
    image = load_image(image_path)
    flat_image = flatten_array(image)
    bits = retrieve_least_significant_bits(flat_image)
    return decode_bits(bits)
```

</details>

## Step 6 ⋅ The `steganosaure` Command

What remains is to turn `encrypt` and `decrypt` into a command line tool, `steganosaure`, with two subcommands:

- `encrypt`, with the arguments `message`, `input_image_path` and `output_image_path`;
- `decrypt`, with the argument `image_path`; it prints the message it finds.

Instructions:

- Create the file `src/steganosaure/cli.py`. Write in it a `create_parser` function, which builds and returns the parser with `argparse` (standard library), and a `main` function, without arguments, which uses it and calls `encrypt` or `decrypt`.
- Declare in `pyproject.toml` the `steganosaure` command, which calls the `main` function of the `steganosaure.cli` module, then run `uv sync` in the Codespace's terminal to install it.
- Create the file `tests/test_cli.py` and test the parser: `create_parser().parse_args(["decrypt", "hidden.png"])` must give the `decrypt` command and the `hidden.png` path.
- Try the command in the Codespace's terminal: `encrypt` creates the image `/tmp/hidden.png`, then `decrypt` finds the message in it.

```console
$ uv run steganosaure encrypt "Hello" tests/images/museum.jpg /tmp/hidden.png
$ uv run steganosaure decrypt /tmp/hidden.png
Hello
```

To go further, rewrite the interface with `Typer` (`uv add typer`, one function per command) and test it with `typer.testing.CliRunner`.

Useful documentation:

- [`argparse`: sub-commands](https://docs.python.org/3/library/argparse.html#subcommands)
- [Declaring a command: `[project.scripts]`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#creating-executable-scripts)
- [`Typer`: multiple commands](https://typer.tiangolo.com/tutorial/commands/), [testing](https://typer.tiangolo.com/tutorial/testing/)

<details>
<summary>Solution</summary>

`src/steganosaure/cli.py`:

```python
"""Steganosaure command line interface."""

from argparse import ArgumentParser
from pathlib import Path

from .steganography import decrypt, encrypt


def create_parser() -> ArgumentParser:
    """Build the parser of the steganosaure command and its two subcommands.

    Returns:
        The parser.
    """
    parser = ArgumentParser(prog="steganosaure", description="Hide messages in images")
    subparsers = parser.add_subparsers(help="Commands", dest="command", required=True)

    parser_encode = subparsers.add_parser("encrypt")
    parser_encode.add_argument("message")
    parser_encode.add_argument("input_image_path", type=Path)
    parser_encode.add_argument("output_image_path", type=Path)

    parser_decode = subparsers.add_parser("decrypt")
    parser_decode.add_argument("image_path", type=Path)
    return parser


def main() -> None:
    """Entrypoint of the program."""
    parser = create_parser()
    args = parser.parse_args()
    if args.command == "encrypt":
        encrypt(args.message, args.input_image_path, args.output_image_path)
    else:
        print(decrypt(args.image_path))
```

`pyproject.toml`:

```toml
[project.scripts]
steganosaure = "steganosaure.cli:main"
```

`tests/test_cli.py`:

```python
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
```

</details>

## Image credits

See [`tests/images/README.md`](tests/images/README.md).
