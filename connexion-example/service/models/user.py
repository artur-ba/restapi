import typing

import pydantic
import sqlalchemy

from service.models import base


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


class UserDB(base.BaseModel):
    __tablename__ = 'users'

    id = sqlalchemy.Column(
        sqlalchemy.String(36),
        nullable=False,
        primary_key=True,
    )
    user_name = sqlalchemy.Column(sqlalchemy.String(25), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    first_name = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    last_name = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
    address = sqlalchemy.Column(sqlalchemy.String(), nullable=True)
    postal_code = sqlalchemy.Column(sqlalchemy.String(), nullable=True)
