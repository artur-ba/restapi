from flask_restful import fields
import sqlalchemy

from service.models import base

USER_FIELDS = {
    'id': fields.String(attribute='id'),
    'userName': fields.String(attribute='user_name'),
    'email': fields.String(attribute='email'),
    'firstName': fields.String(attribute='first_name'),
    'lastName': fields.String(attribute='last_name'),
    'address': fields.String(attribute='address'),
    'postalCode': fields.String(attribute='postal_code'),
}


class User(base.BaseModel):
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
