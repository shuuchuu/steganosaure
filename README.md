# Création d'une CLI de stéganographie

*[English version](https://github.com/shuuchuu/steganosaure/tree/main-en)*

La [stéganographie](https://fr.wikipedia.org/wiki/St%C3%A9ganographie) regroupe les techniques permettant de dissimuler un message. Elle se distingue de la cryptographie, qui ne cherche pas à cacher un message mais à le rendre incompréhensible pour qui ne possède pas la clé nécessaire.

La méthode que nous allons implémenter dans ces travaux pratiques est bien connue : elle consiste à [modifier le bit de poids faible de chaque pixel d'une image](https://fr.wikipedia.org/wiki/St%C3%A9ganographie#Usage_des_bits_de_poids_faible_d'une_image). Cette modification n'est pas visible à l'œil nu (même si elle peut être détectée par une analyse statistique).

Ce README est l'énoncé des travaux pratiques, pour les faire dans un Codespace GitHub ou un clone local ; c'est le même que celui du [notebook des travaux pratiques](https://colab.research.google.com/github/shuuchuu/labs/blob/main/cli-hands-on-fr.ipynb). La [branche `solution`](https://github.com/shuuchuu/steganosaure/tree/solution) en donne une solution, que reprend la section *Solution* de chaque étape. Elle utilise aussi [`deal`](https://deal.readthedocs.io/), que l'énoncé ne demande pas : ses contrats (`@deal.raises`) déclarent les exceptions qu'une fonction peut lever (`uv add deal`).

## Environnement de travail

Pour les TPs, nous utiliserons GitHub Codespaces, qui fournit des instances de VSCode dans des conteneurs. La version gratuite des comptes personnels donne 120 heures-cœurs par mois, soit 60 heures sur la machine à 2 cœurs de ce TP, et 15 Go de stockage. C'est largement suffisant pour ces travaux pratiques.

Si vous n'avez pas de compte GitHub, commencez par en créer un [ici](https://github.com/signup).

Ouvrez le dépôt dans un Codespace : [ce lien](https://codespaces.new/shuuchuu/steganosaure), ou, sur GitHub, **Code** > **Codespaces** > **Create codespace on main**. Dans un clone local, installez [uv](https://docs.astral.sh/uv/getting-started/installation/), puis lancez `uv sync` à la racine du dépôt.

[![Ouvrir dans GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/shuuchuu/steganosaure)

Le dépôt du TP est un projet `uv` : le code va dans `src/steganosaure/` et les tests dans `tests/`. Il ne déclare encore aucune dépendance : dans le terminal du Codespace, `uv add numpy scikit-image` ajoute celles dont ce TP a besoin.

Les tests se lancent depuis ce terminal avec `uv run pytest` (`pytest` est déjà dans les dépendances de développement du dépôt). Le fichier `tests/conftest.py` fournit deux fixtures pytest, `museum_image_path` et `size_image_path`, les chemins des images de `tests/images/` dont l'étape 2 a besoin : un test les reçoit en les nommant parmi ses paramètres.

## Étape 1 ⋅ Fonctions de conversion de chaînes de caractères en bits et inversement

Dans un premier temps, nous allons nous concentrer sur la conversion de chaînes de caractères en bits (et inversement).

Une première fonction, `encode_string`, prendra en argument une chaîne de caractères et renverra un tableau numpy des bits correspondants (dans l'encodage utf8).

Un tableau numpy est une structure de données homogène (éléments de même type), que nous utiliserons dans ces travaux pratiques comme une liste très améliorée.

Par exemple, pour la chaîne `"ABC"`, on attend le tableau de sortie suivant :

```python
numpy.array([0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1])
```

En effet, `A` s'encode `01000001` en utf8, `B` `01000010` et `C` `01000011`. Le tableau attendu est simplement la concaténation de ces bits.

Pour coder cette fonction, voici quelques fonctions utiles :
- [`str.encode`](https://docs.python.org/fr/3/library/stdtypes.html#str.encode), qui renvoie un objet `bytes` (lui-même un itérable d'octets représentés par des entiers)
- [`numpy.unpackbits`](https://numpy.org/doc/stable/reference/generated/numpy.unpackbits.html), que vous pouvez appliquer à un tableau numpy créé au préalable à partir des octets représentés par des entiers obtenus depuis l'objet `bytes`. Pour créer le tableau numpy, vous pouvez utiliser [`numpy.array`](https://numpy.org/doc/stable/reference/generated/numpy.array.html) ou [`numpy.fromiter`](https://numpy.org/doc/stable/reference/generated/numpy.fromiter.html) en précisant `dtype="uint8"` lors de l'appel. Cet argument vous permettra de représenter les valeurs des octets avec le type le plus adapté.

Voici la signature attendue de la fonction :

```python
def encode_string(string: str) -> numpy.ndarray: ...
```

La fonction `decode_bits` se chargera de la transformation inverse. Les fonctions à utiliser sont les inverses de celles nécessaires pour `encode_string` :
- [`bytes.decode`](https://docs.python.org/fr/3/library/stdtypes.html#bytes.decode), qui renvoie une chaîne de caractères
- [`numpy.packbits`](https://numpy.org/doc/stable/reference/generated/numpy.packbits.html)

Voici la signature attendue de la fonction :

```python
def decode_bits(bits: numpy.ndarray) -> str: ...
```

Consignes :

- Créez le fichier `tests/test_string_conversion.py` et écrivez au moins un cas de test par fonction, en utilisant l'exemple donné si besoin. Pour comparer deux tableaux numpy, vous pouvez utiliser la fonction dédiée [`numpy.testing.assert_array_equal`](https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_array_equal.html).
- Créez le fichier `src/steganosaure/string_conversion.py` et implémentez-y ces deux fonctions pour que les tests passent.
- Pouvez-vous concevoir un test qui s'assure que les deux fonctions sont bien inverses l'une de l'autre ? Avec [`hypothesis`](https://hypothesis.readthedocs.io/) (`uv add --dev hypothesis`), il peut porter sur des chaînes générées : `@hypothesis.given(hypothesis.strategies.text())`.

<details>
<summary>Solution</summary>

`tests/test_string_conversion.py` :

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

`src/steganosaure/string_conversion.py` :

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

`decode_bits` retire déjà les caractères nuls de l'étape 5 : les chaînes générées les excluent.

</details>

## Étape 2 ⋅ Fonctions de chargement et de sauvegarde d'images

Nous allons maintenant coder deux fonctions importantes : l'une chargera une image, l'autre la sauvegardera.

**Attention, pour que notre algorithme fonctionne, une image sauvegardée puis rechargée doit être identique à l'image d'origine.**

La fonction de chargement devra charger une image dans un tableau numpy dont les éléments sont des entiers 8 bits (pour cela, vous pouvez utiliser le paquet [`scikit-image`](https://scikit-image.org/), et en particulier les fonctions [`skimage.io.imread`](https://scikit-image.org/docs/stable/api/skimage.io.html#skimage.io.imread) et [`skimage.util.img_as_ubyte`](https://scikit-image.org/docs/stable/api/skimage.util.html#skimage.util.img_as_ubyte)). Voici la signature attendue :

```python
def load_image(image_path: pathlib.Path) -> numpy.ndarray: ...
```

La fonction de sauvegarde devra sauvegarder un tableau numpy au chemin indiqué. Notez que pour que l'image rechargée soit équivalente à l'image sauvegardée tout en gardant une bonne qualité, il est préférable de sauvegarder les images au format `.png`. Vous pouvez utiliser la fonction [`skimage.io.imsave`](https://scikit-image.org/docs/stable/api/skimage.io.html#skimage.io.imsave). Il sera utile de lui passer l'argument `check_contrast=False`. Voici la signature attendue :

```python
def save_image(image: numpy.ndarray, image_path: pathlib.Path) -> None: ...
```

Consignes :

- Créez le fichier `tests/test_image_io.py` et écrivez au moins un cas de test qui s'assure que le point crucial est respecté (une image sauvegardée puis chargée est identique à l'image d'origine).
- Créez le fichier `src/steganosaure/image_io.py` et implémentez-y ces deux fonctions pour que le ou les tests passent.

<details>
<summary>Solution</summary>

`tests/test_image_io.py` :

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

`src/steganosaure/image_io.py` :

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

## Étape 3 ⋅ Fonctions de manipulation de bits

Nous allons maintenant implémenter le cœur de l'algorithme : modifier le bit de poids faible de chaque pixel pour y stocker un bit d'information de la chaîne à cacher.

Petit rappel sur la manipulation de bits :

```python
0b01 & 0b11 == 0b01  # ET bit à bit : le bit résultat vaut 1 si les deux bits valent 1
0b01 | 0b11 == 0b11  # OU bit à bit : le bit résultat vaut 1 si au moins un bit vaut 1
0b11 >> 1 == 0b01  # décalage à droite, complète avec des 0
0b11 << 1 == 0b110  # décalage à gauche, complète avec des 0
```

Ces représentations sont équivalentes à leur notation décimale :

```python
1 & 3 == 1
1 | 3 == 3
3 >> 1 == 1
3 << 1 == 6
```

Pour cela, nous allons implémenter deux fonctions. La première, `retrieve_least_significant_bits`, renverra un tableau numpy de même taille que son argument mais ne contenant que des 0 ou des 1 : les bits de poids faible des nombres contenus dans le tableau en argument.

Pour écrire cette fonction, n'hésitez pas à tirer parti du fait qu'on peut appliquer directement une opération à un tableau numpy (y compris les opérations bit à bit) :

```pycon
>>> 3 & 1
1
>>> 2 & 1
0
>>> numpy.array([3, 2]) & 1
array([1, 0])
```

Voici sa signature attendue :

```python
def retrieve_least_significant_bits(array: numpy.ndarray) -> numpy.ndarray: ...
```

La seconde fonction à implémenter, `modify_least_significant_bits`, modifiera les bits de poids faible de `image` pour qu'ils correspondent au tableau `message`. Voici sa signature attendue :

```python
def modify_least_significant_bits(
    message: numpy.ndarray, image: numpy.ndarray
) -> numpy.ndarray: ...
```

Consignes :

- Créez le fichier `tests/test_bits_manipulation.py` et écrivez au moins un cas de test par fonction.
- Créez le fichier `src/steganosaure/bits_manipulation.py` et implémentez-y ces deux fonctions pour que les tests passent.

<details>
<summary>Solution</summary>

`tests/test_bits_manipulation.py` :

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

`src/steganosaure/bits_manipulation.py` :

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

## Étape 4 ⋅ Fonctions de manipulation de tableaux numpy

La fonction suivante, `pad_array`, prépare les arguments de `modify_least_significant_bits` pour qu'ils aient la même taille. Elle renvoie `small_array` (qui sera notre message à cacher) complété avec des zéros jusqu'à la taille de `big_array` (qui sera l'image dans laquelle le message est dissimulé). Vous pouvez utiliser [`numpy.pad`](https://numpy.org/doc/stable/reference/generated/numpy.pad.html) pour l'implémentation.

Si `small_array` est plus grand que `big_array`, le message ne tient pas dans l'image : `pad_array` doit alors lever une `ValueError` dont le message donne les deux tailles.

Voici sa signature attendue :

```python
def pad_array(
    small_array: numpy.ndarray, big_array: numpy.ndarray
) -> numpy.ndarray: ...
```

Consignes :

- Créez le fichier `tests/test_array_reshaping.py` et écrivez au moins un cas de test pour le complément par des zéros, et un qui vérifie la `ValueError` avec [`pytest.raises`](https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions).
- Créez le fichier `src/steganosaure/array_reshaping.py` et implémentez-y cette fonction pour que les tests passent.

<details>
<summary>Solution</summary>

`tests/test_array_reshaping.py` :

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

`src/steganosaure/array_reshaping.py` :

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

## Étape 5 ⋅ Implémentation de la stéganographie

Nous avons maintenant terminé la phase préparatoire et disposons de toutes les fonctions nécessaires pour implémenter la stéganographie.

La première fonction de notre outil, `encrypt`, permettra à l'utilisateur de cacher un message dans une image. Avant d'appliquer les méthodes déjà développées, il faudra utiliser [`numpy.reshape`](https://numpy.org/doc/stable/reference/generated/numpy.reshape.html) pour obtenir toutes les valeurs de pixels dans un tableau à une dimension, puis pour rendre à l'image modifiée sa forme d'origine. Vous pouvez ranger ces deux opérations dans `array_reshaping.py` (`flatten_array`, `reshape_array`).

Voici sa signature attendue :

```python
def encrypt(
    message: str, input_image_path: pathlib.Path, output_image_path: pathlib.Path
) -> None: ...
```

La seconde fonction de notre outil, `decrypt`, permettra à l'utilisateur de retrouver le message précédemment caché dans une image. Voici sa signature attendue :

```python
def decrypt(image_path: pathlib.Path) -> str: ...
```

L'image contient le message suivi des zéros ajoutés par `pad_array` : décodés, ils donnent des caractères nuls (`"\x00"`) en fin de chaîne. Retirez-les (`str.rstrip("\x00")`), dans `decrypt` ou dans `decode_bits` ; dans le second cas, excluez ce caractère des chaînes générées à l'étape 1 : `hypothesis.strategies.text(hypothesis.strategies.characters(exclude_categories=["Cs"], exclude_characters="\x00"))`. Les substituts (catégorie `Cs`), que `text()` exclut de lui-même, ne s'encodent pas en utf8 : un `characters` sans `exclude_categories` les génère.

Consignes :

- Créez le fichier `tests/test_steganography.py` et écrivez au moins un cas de test qui vérifie le bon fonctionnement des deux fonctions ensemble.
- Créez le fichier `src/steganosaure/steganography.py` et implémentez-y ces deux fonctions pour que les tests passent.

<details>
<summary>Solution</summary>

`src/steganosaure/array_reshaping.py`, après les imports :

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

`tests/test_steganography.py` :

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

`src/steganosaure/steganography.py` :

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

## Étape 6 ⋅ La commande `steganosaure`

Il reste à faire de `encrypt` et `decrypt` un outil en ligne de commande, `steganosaure`, à deux sous-commandes :

- `encrypt`, avec les arguments `message`, `input_image_path` et `output_image_path` ;
- `decrypt`, avec l'argument `image_path` ; elle affiche le message trouvé.

Consignes :

- Créez le fichier `src/steganosaure/cli.py`. Écrivez-y une fonction `create_parser`, qui construit et renvoie le parser avec `argparse` (bibliothèque standard), et une fonction `main`, sans argument, qui l'utilise et appelle `encrypt` ou `decrypt`.
- Déclarez dans `pyproject.toml` la commande `steganosaure`, qui appelle la fonction `main` du module `steganosaure.cli`, puis lancez `uv sync` dans le terminal du Codespace pour l'installer.
- Créez le fichier `tests/test_cli.py` et testez le parser : `create_parser().parse_args(["decrypt", "cache.png"])` doit donner la commande `decrypt` et le chemin `cache.png`.
- Essayez la commande dans le terminal du Codespace : `encrypt` crée l'image `/tmp/cache.png`, puis `decrypt` y retrouve le message.

```console
$ uv run steganosaure encrypt "Bonjour" tests/images/museum.jpg /tmp/cache.png
$ uv run steganosaure decrypt /tmp/cache.png
Bonjour
```

Pour aller plus loin, réécrivez l'interface avec `Typer` (`uv add typer`, une fonction par commande) et testez-la avec `typer.testing.CliRunner`.

Documentation utile :

- [`argparse` : sous-commandes](https://docs.python.org/fr/3/library/argparse.html#subcommands)
- [Déclarer une commande : `[project.scripts]`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#creating-executable-scripts)
- [`Typer` : plusieurs commandes](https://typer.tiangolo.com/tutorial/commands/), [tests](https://typer.tiangolo.com/tutorial/testing/)

<details>
<summary>Solution</summary>

`src/steganosaure/cli.py` :

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

`pyproject.toml` :

```toml
[project.scripts]
steganosaure = "steganosaure.cli:main"
```

`tests/test_cli.py` :

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

## Crédits des images

Voir [`tests/images/README.md`](tests/images/README.md).
