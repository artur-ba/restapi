import os

from flask import Flask
from flask_restful import Api


application = Flask('service')
api = Api(application)


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=3000, debug=True)
