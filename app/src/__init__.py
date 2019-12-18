
from flask import Flask
from flask_cors import CORS
import os
import logging
import sys
from .database import init_app as initialize_database

from .utils.configuration import load_application_variables, generate_amqp_uri, generate_database_uri
from .api import register_routes

def create_app(env="production") -> Flask:

    app = Flask(__name__)

    # importing the default configuration
    print(env)    
    app.config.from_mapping(load_application_variables(env))
    # depending on environment load the correct configuration
    if env == "production":
        # allow only certain origins or all
        allowed_origins = app.config.get("ALLOWED_ORIGINS")
        if allowed_origins is not None:
            CORS(app, origins = allowed_origins)
        else:
            CORS(app)
        
        @app.route("/")
        def good_api(): # pylint: disable=W0612
            return "It Works!"
    else:
        CORS(app)
        @app.route("/testing")
        def testing(): # pylint: disable=W0612
            return "It Works"

    app.config["DATABASE_URI"] = generate_database_uri(**app.config)
    app.config["BROKER_URI"] = generate_amqp_uri(**app.config)

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
    
    # initialize database
    initialize_database(app)

    # register the api routes
    register_routes(app)
    
    return app



    




