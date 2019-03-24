import logging
import re

import connexion
import ujson

from service.models import database

LOG = logging.getLogger(__name__)

LOG.debug('Initializing aws-service')

application = connexion.App(
    'service',
    debug=False,
)

application.add_api(
    './swagger.yaml',
    strict_validation=True,
    validate_responses=True,
    pythonic_params=True,
)

application.app.config.from_object('service.config')
database.db.init_app(application.app)


@application.app.after_request
def after_request(response: connexion.lifecycle.ConnexionResponse) -> connexion.lifecycle.ConnexionResponse:
    if re.match(r'5|4\d\d', str(response.status_code)) and response.data:
        original = ujson.loads(response.data.decode('utf-8'))

        if 'message' not in original:
            response.data = ujson.dumps({'message': original['detail']})

    response.content_type = 'application/json'
    return response
