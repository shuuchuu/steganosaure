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

Les tests se lancent depuis ce terminal avec `uv run pytest` (`pytest` est déjà dans les dépendances de développement du dépôt). Le fichier `tests/conftest.py` fournit deux fixtures pytest, `chemin_image_musee` et `chemin_image_taille`, les chemins des images de `tests/images/` dont l'étape 2 a besoin : un test les reçoit en les nommant parmi ses paramètres.

## Étape 1 ⋅ Fonctions de conversion de chaînes de caractères en bits et inversement

Dans un premier temps, nous allons nous concentrer sur la conversion de chaînes de caractères en bits (et inversement).

Une première fonction, `encode_chaine`, prendra en argument une chaîne de caractères et renverra un tableau numpy des bits correspondants (dans l'encodage utf8).

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
def encode_chaine(chaine: str) -> numpy.ndarray: ...
```

La fonction `decode_bits` se chargera de la transformation inverse. Les fonctions à utiliser sont les inverses de celles nécessaires pour `encode_chaine` :
- [`bytes.decode`](https://docs.python.org/fr/3/library/stdtypes.html#bytes.decode), qui renvoie une chaîne de caractères
- [`numpy.packbits`](https://numpy.org/doc/stable/reference/generated/numpy.packbits.html)

Voici la signature attendue de la fonction :

```python
def decode_bits(bits: numpy.ndarray) -> str: ...
```

Consignes :

- Créez le fichier `tests/test_conversion_chaines.py` et écrivez au moins un cas de test par fonction, en utilisant l'exemple donné si besoin. Pour comparer deux tableaux numpy, vous pouvez utiliser la fonction dédiée [`numpy.testing.assert_array_equal`](https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_array_equal.html).
- Créez le fichier `src/steganosaure/conversion_chaines.py` et implémentez-y ces deux fonctions pour que les tests passent.
- Pouvez-vous concevoir un test qui s'assure que les deux fonctions sont bien inverses l'une de l'autre ? Avec [`hypothesis`](https://hypothesis.readthedocs.io/) (`uv add --dev hypothesis`), il peut porter sur des chaînes générées : `@hypothesis.given(hypothesis.strategies.text())`.

<details>
<summary>Solution</summary>

`tests/test_conversion_chaines.py` :

```python
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
```

`src/steganosaure/conversion_chaines.py` :

```python
"""Conversion de chaînes de caractères en bits, et inversement."""

import deal
import numpy


def encode_chaine(chaine: str) -> numpy.ndarray:
    """Convertit une chaîne (utf8) en tableau numpy de bits.

    Args:
        chaine: La chaîne à convertir.

    Returns:
        Tableau numpy de dtype uint8 (numpy n'a pas de vrai type booléen) qui contient
        les bits utf8 (pas les octets, donc des 0 et des 1) de la chaîne d'entrée.
    """
    return numpy.unpackbits(numpy.array(list(chaine.encode("utf8")), dtype="uint8"))


@deal.raises(UnicodeDecodeError)
def decode_bits(bits: numpy.ndarray) -> str:
    """Reconvertit un tableau numpy de bits en chaîne.

    Args:
        bits: Tableau numpy de dtype uint8 qui ne contient que des 0 et des 1
              représentant de l'utf8 valide.

    Returns:
        La chaîne correspondante.
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
def charge_image(chemin_image: pathlib.Path) -> numpy.ndarray: ...
```

La fonction de sauvegarde devra sauvegarder un tableau numpy au chemin indiqué. Notez que pour que l'image rechargée soit équivalente à l'image sauvegardée tout en gardant une bonne qualité, il est préférable de sauvegarder les images au format `.png`. Vous pouvez utiliser la fonction [`skimage.io.imsave`](https://scikit-image.org/docs/stable/api/skimage.io.html#skimage.io.imsave). Il sera utile de lui passer l'argument `check_contrast=False`. Voici la signature attendue :

```python
def sauvegarde_image(image: numpy.ndarray, chemin_image: pathlib.Path) -> None: ...
```

Consignes :

- Créez le fichier `tests/test_images.py` et écrivez au moins un cas de test qui s'assure que le point crucial est respecté (une image sauvegardée puis chargée est identique à l'image d'origine).
- Créez le fichier `src/steganosaure/images.py` et implémentez-y ces deux fonctions pour que le ou les tests passent.

<details>
<summary>Solution</summary>

`tests/test_images.py` :

```python
import pathlib

import hypothesis
import hypothesis.extra.numpy
import hypothesis.strategies
import numpy
import pytest

from steganosaure.images import charge_image, sauvegarde_image


@hypothesis.settings(deadline=None)
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
```

`src/steganosaure/images.py` :

```python
"""Chargement et sauvegarde d'images."""

import pathlib
import sys

import numpy
import skimage


def charge_image(chemin_image: pathlib.Path) -> numpy.ndarray:
    """Charge une image dans un tableau numpy.

    Args:
        chemin_image: Chemin de l'image à charger.

    Returns:
        Un tableau numpy de dtype uint8, de dimensions (hauteur, largeur, canaux).
    """
    return skimage.util.img_as_ubyte(skimage.io.imread(chemin_image))


def sauvegarde_image(image: numpy.ndarray, chemin_image: pathlib.Path) -> None:
    """Sauvegarde une image.

    Args:
        image: Tableau numpy qui représente l'image à sauvegarder.
        chemin_image: Chemin de l'image de sortie, de préférence un .png : un format
            avec perte comme le .jpg change les bits de poids faible, et perd le
            message caché.
    """
    if chemin_image.suffix.lower() != ".png":
        print(
            f"{chemin_image} n'est pas un .png : un format avec perte perd le message",
            file=sys.stderr,
        )
    skimage.io.imsave(chemin_image, image, check_contrast=False)
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

Pour cela, nous allons implémenter deux fonctions. La première, `extrait_bits_poids_faible`, renverra un tableau numpy de même taille que son argument mais ne contenant que des 0 ou des 1 : les bits de poids faible des nombres contenus dans le tableau en argument.

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
def extrait_bits_poids_faible(tableau: numpy.ndarray) -> numpy.ndarray: ...
```

La seconde fonction à implémenter, `modifie_bits_poids_faible`, modifiera les bits de poids faible de `image` pour qu'ils correspondent au tableau `message`. Voici sa signature attendue :

```python
def modifie_bits_poids_faible(
    message: numpy.ndarray, image: numpy.ndarray
) -> numpy.ndarray: ...
```

Consignes :

- Créez le fichier `tests/test_manipulation_bits.py` et écrivez au moins un cas de test par fonction.
- Créez le fichier `src/steganosaure/manipulation_bits.py` et implémentez-y ces deux fonctions pour que les tests passent.

<details>
<summary>Solution</summary>

`tests/test_manipulation_bits.py` :

```python
"""Manipulation de bits."""

import numpy

from steganosaure.manipulation_bits import (
    extrait_bits_poids_faible,
    modifie_bits_poids_faible,
)


def test_extrait_bits_poids_faible() -> None:
    numpy.testing.assert_array_equal(
        extrait_bits_poids_faible(numpy.array([1, 3, 2])), numpy.array([1, 1, 0])
    )


def test_modifie_bits_poids_faible() -> None:
    numpy.testing.assert_array_equal(
        modifie_bits_poids_faible(numpy.array([1, 1, 0]), numpy.array([1, 2, 3])),
        numpy.array([1, 3, 2]),
    )
```

`src/steganosaure/manipulation_bits.py` :

```python
"""Manipulation de bits."""

import numpy


def extrait_bits_poids_faible(tableau: numpy.ndarray) -> numpy.ndarray:
    """Extrait les bits de poids faible de tous les éléments d'un tableau numpy.

    Par exemple, pour le tableau numpy.array([1, 2, 3]), elle renvoie
    numpy.array([1, 0, 1]). En effet, 1, 2 et 3 s'écrivent 00000001, 00000010 et
    00000011 en binaire : si on ne garde que le dernier bit, on obtient 1, 0 et 1.

    Args:
        tableau: Tableau numpy de nombres (qui acceptent l'opérateur binaire &).

    Returns:
        Un tableau numpy de même dtype que le tableau d'entrée, où seuls les bits de
        poids faible sont gardés.
    """
    return tableau & 1


def modifie_bits_poids_faible(
    message: numpy.ndarray, image: numpy.ndarray
) -> numpy.ndarray:
    """Modifie les bits de poids faible du tableau image pour y écrire le message.

    Par exemple, pour les tableaux :

    - message : numpy.array([1, 1, 0])
    - image : numpy.array([1, 2, 3])

    Elle renvoie numpy.array([1, 3, 2]). En effet, 1, 2 et 3 s'écrivent 00000001,
    00000010 et 00000011 en binaire : quand on met leur dernier bit à 1, 1 et 0, on
    obtient 00000001, 00000011 et 00000010, soit 1, 3 et 2 en décimal.

    Args:
        message: Tableau numpy de bits (des 0 et des 1).
        image: Tableau numpy de nombres (qui acceptent les opérateurs binaires >>, <<
            et |).

    Returns:
        Un tableau numpy du dtype le plus général des deux tableaux d'entrée, avec les
        bits de message en poids faible et tous les autres bits de image.
    """
    return image >> 1 << 1 | message
```

</details>

## Étape 4 ⋅ Fonctions de manipulation de tableaux numpy

La fonction suivante, `complete_tableau`, prépare les arguments de `modifie_bits_poids_faible` pour qu'ils aient la même taille. Elle renvoie `petit_tableau` (qui sera notre message à cacher) complété avec des zéros jusqu'à la taille de `grand_tableau` (qui sera l'image dans laquelle le message est dissimulé). Vous pouvez utiliser [`numpy.pad`](https://numpy.org/doc/stable/reference/generated/numpy.pad.html) pour l'implémentation.

Si `petit_tableau` est plus grand que `grand_tableau`, le message ne tient pas dans l'image : `complete_tableau` doit alors lever une `ValueError` dont le message donne les deux tailles.

Voici sa signature attendue :

```python
def complete_tableau(
    petit_tableau: numpy.ndarray, grand_tableau: numpy.ndarray
) -> numpy.ndarray: ...
```

Consignes :

- Créez le fichier `tests/test_manipulation_tableaux.py` et écrivez au moins un cas de test pour le complément par des zéros, et un qui vérifie la `ValueError` avec [`pytest.raises`](https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions).
- Créez le fichier `src/steganosaure/manipulation_tableaux.py` et implémentez-y cette fonction pour que les tests passent.

<details>
<summary>Solution</summary>

`tests/test_manipulation_tableaux.py` :

```python
import numpy
import pytest

from steganosaure.manipulation_tableaux import complete_tableau


def test_complete_tableau() -> None:
    numpy.testing.assert_array_equal(
        complete_tableau(numpy.array([1, 1, 0]), numpy.arange(10)),
        numpy.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
    )


def test_complete_tableau_trop_grand() -> None:
    with pytest.raises(ValueError, match="10 > 3"):
        complete_tableau(numpy.arange(10), numpy.array([1, 1, 0]))
```

`src/steganosaure/manipulation_tableaux.py` :

```python
"""Manipulation de tableaux numpy."""

import deal
import numpy


@deal.raises(ValueError)
def complete_tableau(
    petit_tableau: numpy.ndarray, grand_tableau: numpy.ndarray
) -> numpy.ndarray:
    """Complète le petit tableau par des 0 jusqu'à la taille du grand tableau.

    Args:
        petit_tableau: Tableau numpy de nombres.
        grand_tableau: Tableau numpy.

    Returns:
        Un tableau numpy de même dtype et de mêmes premiers éléments que petit_tableau,
        de la taille de grand_tableau.

    Raises:
        ValueError: Si petit_tableau est plus grand que grand_tableau (le message ne
            tient pas dans l'image).
    """
    if petit_tableau.size > grand_tableau.size:
        msg = (
            "Le tableau à compléter est plus grand que le tableau de référence : "
            f"{petit_tableau.size} > {grand_tableau.size}"
        )
        raise ValueError(msg)
    return numpy.pad(petit_tableau, (0, grand_tableau.size - petit_tableau.size))
```

</details>

## Étape 5 ⋅ Implémentation de la stéganographie

Nous avons maintenant terminé la phase préparatoire et disposons de toutes les fonctions nécessaires pour implémenter la stéganographie.

La première fonction de notre outil, `chiffre`, permettra à l'utilisateur de cacher un message dans une image. Avant d'appliquer les méthodes déjà développées, il faudra utiliser [`numpy.reshape`](https://numpy.org/doc/stable/reference/generated/numpy.reshape.html) pour obtenir toutes les valeurs de pixels dans un tableau à une dimension, puis pour rendre à l'image modifiée sa forme d'origine. Vous pouvez ranger ces deux opérations dans `manipulation_tableaux.py` (`aplatit_tableau`, `reforme_tableau`).

Voici sa signature attendue :

```python
def chiffre(
    message: str, chemin_image_entree: pathlib.Path, chemin_image_sortie: pathlib.Path
) -> None: ...
```

La seconde fonction de notre outil, `dechiffre`, permettra à l'utilisateur de retrouver le message précédemment caché dans une image. Voici sa signature attendue :

```python
def dechiffre(chemin_image: pathlib.Path) -> str: ...
```

L'image contient le message suivi des zéros ajoutés par `complete_tableau` : décodés, ils donnent des caractères nuls (`"\x00"`) en fin de chaîne. Retirez-les (`str.rstrip("\x00")`), dans `dechiffre` ou dans `decode_bits` ; dans le second cas, excluez ce caractère des chaînes générées à l'étape 1 : `hypothesis.strategies.text(hypothesis.strategies.characters(exclude_categories=["Cs"], exclude_characters="\x00"))`. Les substituts (catégorie `Cs`), que `text()` exclut de lui-même, ne s'encodent pas en utf8 : un `characters` sans `exclude_categories` les génère.

Consignes :

- Créez le fichier `tests/test_steganographie.py` et écrivez au moins un cas de test qui vérifie le bon fonctionnement des deux fonctions ensemble.
- Créez le fichier `src/steganosaure/steganographie.py` et implémentez-y ces deux fonctions pour que les tests passent.

<details>
<summary>Solution</summary>

`src/steganosaure/manipulation_tableaux.py`, après les imports :

```python
def aplatit_tableau(tableau: numpy.ndarray) -> numpy.ndarray:
    """Aplatit le tableau donné pour qu'il n'ait qu'une dimension.

    Args:
        tableau: Tableau numpy à aplatir.

    Returns:
        Tableau plat.
    """
    return tableau.flatten()


def reforme_tableau(
    tableau_plat: numpy.ndarray, forme: tuple[int, ...]
) -> numpy.ndarray:
    """Rend à un tableau sa forme d'origine.

    Args:
        tableau_plat: Tableau numpy plat.
        forme: Forme à rendre.

    Returns:
        Le tableau remis en forme.
    """
    return tableau_plat.reshape(forme)
```

`tests/test_steganographie.py` :

```python
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
```

`src/steganosaure/steganographie.py` :

```python
"""Fonctions principales de l'outil steganosaure : chiffrer et déchiffrer un message."""

import pathlib

import deal

from .conversion_chaines import decode_bits, encode_chaine
from .images import charge_image, sauvegarde_image
from .manipulation_bits import (
    extrait_bits_poids_faible,
    modifie_bits_poids_faible,
)
from .manipulation_tableaux import aplatit_tableau, complete_tableau, reforme_tableau


@deal.raises(ValueError, FileNotFoundError)
def chiffre(
    message: str, chemin_image_entree: pathlib.Path, chemin_image_sortie: pathlib.Path
) -> None:
    """Chiffre un message dans une image.

    Si le message ne tient pas dans l'image, complete_tableau lève une ValueError.

    Args:
        message: Message à chiffrer.
        chemin_image_entree: Image qui servira à cacher le message.
        chemin_image_sortie: Image résultat, où le message sera caché.
    """
    image_entree = charge_image(chemin_image_entree)
    tableau_message = encode_chaine(message)
    image_plate = aplatit_tableau(image_entree)
    tableau_complete = complete_tableau(tableau_message, image_plate)
    nouvelle_image = modifie_bits_poids_faible(tableau_complete, image_plate)
    image_sortie = reforme_tableau(nouvelle_image, image_entree.shape)
    sauvegarde_image(image_sortie, chemin_image_sortie)


def dechiffre(chemin_image: pathlib.Path) -> str:
    """Déchiffre le message d'une image (ou du moins, essaie).

    Args:
        chemin_image: Image à déchiffrer.

    Returns:
        La chaîne déchiffrée.
    """
    image = charge_image(chemin_image)
    image_plate = aplatit_tableau(image)
    bits = extrait_bits_poids_faible(image_plate)
    return decode_bits(bits)
```

</details>

## Étape 6 ⋅ La commande `steganosaure`

Il reste à faire de `chiffre` et `dechiffre` un outil en ligne de commande, `steganosaure`, à deux sous-commandes :

- `chiffre`, avec les arguments `message`, `chemin_image_entree` et `chemin_image_sortie` ;
- `dechiffre`, avec l'argument `chemin_image` ; elle affiche le message trouvé.

Consignes :

- Créez le fichier `src/steganosaure/cli.py`. Écrivez-y une fonction `cree_parseur`, qui construit et renvoie le parseur avec `argparse` (bibliothèque standard), et une fonction `main`, sans argument, qui l'utilise et appelle `chiffre` ou `dechiffre`.
- Déclarez dans `pyproject.toml` la commande `steganosaure`, qui appelle la fonction `main` du module `steganosaure.cli`, puis lancez `uv sync` dans le terminal du Codespace pour l'installer.
- Créez le fichier `tests/test_cli.py` et testez le parseur : `cree_parseur().parse_args(["dechiffre", "cache.png"])` doit donner la commande `dechiffre` et le chemin `cache.png`.
- Essayez la commande dans le terminal du Codespace : `chiffre` crée l'image `/tmp/cache.png`, puis `dechiffre` y retrouve le message.

```console
$ uv run steganosaure chiffre "Bonjour" tests/images/musee.jpg /tmp/cache.png
$ uv run steganosaure dechiffre /tmp/cache.png
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
"""Interface en ligne de commande de steganosaure."""

from argparse import ArgumentParser
from pathlib import Path

from .steganographie import chiffre, dechiffre


def cree_parseur() -> ArgumentParser:
    """Construit le parseur de la commande steganosaure et de ses deux sous-commandes.

    Returns:
        Le parseur.
    """
    parseur = ArgumentParser(
        prog="steganosaure", description="Cache des messages dans des images"
    )
    sous_parseurs = parseur.add_subparsers(
        help="Commandes", dest="commande", required=True
    )

    parseur_chiffre = sous_parseurs.add_parser("chiffre")
    parseur_chiffre.add_argument("message")
    parseur_chiffre.add_argument("chemin_image_entree", type=Path)
    parseur_chiffre.add_argument("chemin_image_sortie", type=Path)

    parseur_dechiffre = sous_parseurs.add_parser("dechiffre")
    parseur_dechiffre.add_argument("chemin_image", type=Path)
    return parseur


def main() -> None:
    """Point d'entrée du programme."""
    parseur = cree_parseur()
    args = parseur.parse_args()
    if args.commande == "chiffre":
        chiffre(args.message, args.chemin_image_entree, args.chemin_image_sortie)
    else:
        print(dechiffre(args.chemin_image))
```

`pyproject.toml` :

```toml
[project.scripts]
steganosaure = "steganosaure.cli:main"
```

`tests/test_cli.py` :

```python
import pathlib

from steganosaure.cli import cree_parseur


def test_analyse_dechiffre() -> None:
    args = cree_parseur().parse_args(["dechiffre", "cache.png"])
    assert args.commande == "dechiffre"
    assert args.chemin_image == pathlib.Path("cache.png")


def test_analyse_chiffre() -> None:
    args = cree_parseur().parse_args(["chiffre", "Bonjour", "musee.jpg", "cache.png"])
    assert args.commande == "chiffre"
    assert args.message == "Bonjour"
    assert args.chemin_image_entree == pathlib.Path("musee.jpg")
    assert args.chemin_image_sortie == pathlib.Path("cache.png")
```

</details>

## Crédits des images

Voir [`tests/images/README.md`](tests/images/README.md).
