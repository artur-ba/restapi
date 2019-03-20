import logging

import connexion

from service import database
from service import middlewares

LOG = logging.getLogger(__name__)

connexion_app = connexion.AioHttpApp(
    __name__,
    only_one_api=True,
    options={
        'swagger_ui': True,
        'server_spec': True,
        'debug': True,
        'middlewares': middlewares.get(),
    },
)
connexion_app.add_api(
    'swagger.yaml',
    strict_validation=True,
    validate_responses=True,
    pythonic_params=True,
)

application = connexion_app.app
application.cleanup_ctx.append(database.get_db_engine)
