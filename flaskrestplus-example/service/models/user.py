import flask_restplus
import sqlalchemy

from service.models import base

USER_FILEDS = flask_restplus.Model(
    'User',
    {
        'id': flask_restplus.fields.String(attribute='id', required=True, description='User id'),
        'userName': flask_restplus.fields.String(attribute='user_name', required=True, description='User name'),
        'email': flask_restplus.fields.String(attribute='email', required=True, description='User email'),
        'firstName': flask_restplus.fields.String(
            attribute='first_name',
            required=True,
            description='User first name',
        ),
        'lastName': flask_restplus.fields.String(attribute='last_name', required=True, description='User last name'),
        'address': flask_restplus.fields.String(attribute='address', requied=False, description='User address'),
        'postalCode': flask_restplus.fields.String(attribute='postal_code', required=False, description='Postal code'),
    },
)

USER_FILTER = flask_restplus.reqparse.RequestParser()
USER_FILTER.add_argument('lastName', required=False, type=str, location='args')

USER_CREATE_PARSER = flask_restplus.reqparse.RequestParser()
USER_CREATE_PARSER.add_argument(
    'userName',
    dest='user_name',
    required=True,
    type=flask_restplus.inputs.regex('^(?!-)[A-Za-z0-9-_]{1,25}(?<!-)$'),
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
    type=flask_restplus.inputs.regex(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'),
    help='User email is required',
)
USER_CREATE_PARSER.add_argument('address', required=False, type=str)
USER_CREATE_PARSER.add_argument(
    'postalCode',
    dest='postal_code',
    required=False,
    type=flask_restplus.inputs.regex(r'^[\d]{2}-[\d]{3}$'),
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
