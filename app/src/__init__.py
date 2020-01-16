from flask import Flask
from flask_basicauth import BasicAuth
from flask_cors import CORS
import os
import logging
import sys
from .database import init_app as initialize_database

from .utils.configuration import load_application_variables, generate_amqp_uri, generate_database_uri
from .utils.middleware.prefixer import PrefixMiddleware


def create_app(env="production") -> Flask:

    app = Flask(__name__)

    # importing the default configuration
    print(env)    
    app.config.from_mapping(load_application_variables(env))
    # depending on environment load the correct configuration
    CORS(app)

    app.config["DATABASE_URI"] = generate_database_uri(**app.config)
    app.config["BROKER_URI"] = generate_amqp_uri(**app.config)

    # configure sentiment analysis
    if app.config["USE_SENTIMENT"] == "True":
        app.config["USE_SENTIMENT"] = True
    else:
        app.config["USE_SENTIMENT"] = False

    if app.config["USE_SENTIMENT"] is True:
        g_app_credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if g_app_credentials is None:
            raise ValueError(
                "The USE_SENTIMENT flag has been specified as True however, the GOOGLE_APPLICATION_CREDENTIALS " + 
                "was not specified and is required to enable sentiment analysis"
            ) 
        if os.path.isfile(g_app_credentials) is False:
            raise ValueError(
                "The USE_SENTIMENT flag has been specified as True however, the value of GOOGLE_APPLICATION_CREDENTIALS " +
                "is not a valid path."
            )
        app.config["GOOGLE_APPLICATION_CREDENTIALS"] = g_app_credentials
    
    # configure basic auth
    if app.config["BASIC_AUTH_ENABLED"] == "True":
        app.config["BASIC_AUTH_ENABLED"] = True
    else:
        app.config["BASIC_AUTH_ENABLED"] = False

    if app.config["BASIC_AUTH_ENABLED"] is True:
        if app.config.get("BASIC_AUTH_USERNAME") is None:
            raise ValueError(
                "The BASIC_AUTH_ENABLED flag has been specified as True however, BASIC_AUTH_USERNAME was not provided"
            )
        elif app.config.get("BASIC_AUTH_PASSWORD") is None:
            raise ValueError(
                "The BASIC_AUTH_ENABLED flag has been specified as True however, BASIC_AUTH_PASSWORD was not provided"
            )
        elif app.config.get("BASIC_AUTH_REALM") is None:
            raise ValueError(
                "The BASIC_AUTH_ENABLED flag has been specified as True however, BASIC_AUTH_REALM was not provided"
            )
        
        BasicAuth(app=app)
    
    if app.config["ENABLE_FRONT_END"] == "True":
        app.config["ENABLE_FRONT_END"] = True
        app.wsgi_app = PrefixMiddleware(app.wsgi_app)
    else:
        app.config["ENABLE_FRONT_END"] = False

    # initialize database
    initialize_database(app)

    from .worker import CelerySingleton
    celery = CelerySingleton(app).get_celery()

    # import tasks so that they are defined in the celery app
    from src.worker.tasks import add_two_numbers

    # register the api routes
    from .api import register_routes
    register_routes(app)
    
    return app, celery 



    




