import logging
import typing
import uuid

import flask_restplus
from sqlalchemy.orm import exc

from service.models import database
from service.models import user

LOG = logging.getLogger(__name__)

api = flask_restplus.Namespace('users', description='Users related operations')

USER_MODEL = api.model(user.USER_FILEDS.name, user.USER_FILEDS)


@api.route('')
class Users(flask_restplus.Resource):
    @api.doc(
        description='Gets users',
    )
    @api.param('lastName', description='User last name to filter by', _in='query')
    @api.marshal_with(USER_MODEL, code=200)
    def get(self) -> typing.Tuple[typing.List[typing.Dict[str, typing.Any]], int]:
        arguments = user.USER_FILTER.parse_args()
        LOG.info('Received request to list users')
        if arguments['lastName']:
            users = user.User.query.filter(user.User.last_name.like(f'%{arguments["lastName"]}%'))
        else:
            users = user.User.query.all()

        return [u.to_dict() for u in users], 200

    @api.doc(
        description='Creates a new user',
        responses={
            '409': 'User already exist',
            '500': 'Internal server error',
        },
    )
    @api.expect(user.USER_CREATE_PARSER)
    @api.marshal_with(USER_MODEL, code=201)
    def post(self) -> typing.Tuple[typing.Dict[str, typing.Any], int]:
        LOG.info('Received request to create a new user')
        arguments = user.USER_CREATE_PARSER.parse_args()
        try:
            single_user = user.User.query.filter_by(user_name=arguments['user_name']).one()
            if single_user:
                flask_restplus.abort(409, message='User by this name already exists in the system')
        except exc.NoResultFound:
            LOG.info('User doesn\'t exist, system will add it')

        new_user = user.User(**arguments)
        new_user.id = str(uuid.uuid4())
        database.db.session.add(new_user)
        try:
            database.db.session.commit()
            LOG.info('Added new user')
        except Exception:
            LOG.exception('Failed to add user')
            database.db.session.rollback()
            flask_restplus.abort(500, message='Failed to add new user to the system')
        return new_user.to_dict(), 201


@api.route('/<user_id>')
@api.param('user_id', description='User id')
class User(flask_restplus.Resource):
    def _get_user(self, user_id: str) -> user.User:
        try:
            single_user = user.User.query.filter_by(id=user_id).one()
        except exc.NoResultFound:
            LOG.exception('User does not exist')
            flask_restplus.abort(404, message='User does not exist')
        return single_user

    @api.doc(
        description='Get single user by id',
        responses={
            '404': 'User does not exist',
        },
    )
    @api.marshal_with(USER_MODEL, 200)
    def get(self, user_id: str) -> typing.Tuple[typing.List[typing.Dict[str, typing.Any]], int]:
        LOG.info('Received request to get user by id')
        single_user = self._get_user(user_id)
        return single_user.to_dict(), 200

    @api.doc(
        descritpion='Deletes user by id',
        responses={
            '204': 'Deleted user',
            '404': 'User does not exist',
            '500': 'Failed to delete user',
        },
    )
    def delete(self, user_id: str) -> typing.Tuple[typing.Any, int]:
        LOG.info('Received request to delete user')
        single_user = self._get_user(user_id)
        try:
            database.db.session.delete(single_user)
            database.db.session.commit()
        except Exception:
            LOG.exception('Failed to delete user')
            flask_restplus.abort(500, message='Failed to delete user')
        return '', 204
