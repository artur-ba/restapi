import typing

import pydantic


class User(pydantic.BaseModel):
    id: str
    userName: str
    email: str
    firstName: str
    lastName: str
    address: typing.Optional[str] = ''
    postalCode: typing.Optional[str] = ''

    class Config:
        allow_mutation = False
        anystr_strip_whitespace = True

    @staticmethod
    def dumps(obj: typing.Union['pydantic.BaseModel', typing.List['pydantic.BaseModel']]) -> str:
        if isinstance(obj, list):
            return f'[{",".join([o.json() for o in obj])}]'
        else:
            return obj.json()
