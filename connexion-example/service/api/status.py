import typing

import connexion


def get() -> typing.Tuple[typing.Any, int]:
    return connexion.NoContent, 200
