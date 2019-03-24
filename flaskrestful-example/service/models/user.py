from flask_restful import fields
from flask_restful import inputs
from flask_restful import reqparse
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

USER_FILTER = reqparse.RequestParser()
USER_FILTER.add_argument('lastName', required=False, type=str, location='args')

USER_CREATE_PARSER = reqparse.RequestParser()
USER_CREATE_PARSER.add_argument(
    'userName',
    dest='user_name',
    required=True,
    type=inputs.regex('^(?!-)[A-Za-z0-9-_]{1,25}(?<!-)$'),
    help='User name is required',
)
USER_CREATE_PARSER.add_argument(
    'firstName',
    dest='first_name',
    required=True,
    type=str,
    help='User first name is required',
)
USER_CREATE_PARSER.add_argument(
    'lastName',
    dest='last_name',
    required=True,
    type=str,
    help='User last name is required',
)
USER_CREATE_PARSER.add_argument(
    'email',
    dest='email',
    required=True,
    type=inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
    help='User email is required',
)
USER_CREATE_PARSER.add_argument('address', required=False, type=str)
USER_CREATE_PARSER.add_argument(
    'postalCode',
    dest='postal_code',
    required=False,
    type=inputs.regex(r'^[\d]{2}-[\d]{3}$'),
)


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
