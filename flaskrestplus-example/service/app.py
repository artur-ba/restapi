import logging

from flask import Flask

from service.api import api
from service.models import database

LOG = logging.getLogger(__name__)

application = Flask('service')
application.config.from_object('service.config')
application.config['RESTPLUS_VALIDATE'] = True
api.init_app(application)
database.db.init_app(application)
LOG.info('Initialized application')
