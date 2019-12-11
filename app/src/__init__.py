
from flask import Flask
from flask_cors import CORS
import os
import logging
import sys
from .database import init_app as initialize_database
from .utils.errors.messages import CONFIG_IS_WRONG_TYPE, CONFIG_VAR_DOES_NOT_EXIST
from .api import register_routes

def create_app(env="production") -> Flask:

    app = Flask(__name__)


    # importing the default configuration
    from src.config import default
    app.config.from_object(default)

    # depending on environment load the correct configuration
    if env == "production":
        from src.config import production
        app.config.from_object(production)

        # allow only certain origins or all
        allowed_origins = app.config.get("ALLOWED_ORIGINS")
        if allowed_origins is not None:
            if not isinstance(allowed_origins, list):
                raise TypeError(
                    CONFIG_IS_WRONG_TYPE.format(
                        config_var = "ALLOWED_ORIGINS",
                        config_var_type = "list",
                        config_incorrect_type = type(allowed_origins).__name__
                    )
                )
            CORS(app, origins = allowed_origins)
        else:
            CORS(app)
        
        @app.route("/")
        def good_api(): # pylint: disable=W0612
            return "It Works!"
    else:
        from src.config import development
        app.config.from_object(development)
        CORS(app)
        
        @app.route("/testing")
        def testing(): # pylint: disable=W0612
            return "It Works"

    
    # check if database variables exist and then construct the database URI
    
    # DATABASE_NAME 
    DATABASE_NAME = app.config.get("DATABASE_NAME")
    if DATABASE_NAME is None:
        environ_var = os.environ.get("EVALHALLA_DATABASE_NAME")
        if environ_var is None:
            app.config["DATABASE_NAME"] = "evalhalla"
            logging.warn(
                "DATABASE_NAME was not set as a configuration variable or environment variable. " +
                "Defaulting to evalhalla as DATABASE_NAME"    
            )
        else:
            app.config["DATABASE_NAME"] = environ_var
    elif not isinstance(DATABASE_NAME, str):
        raise TypeError(
             CONFIG_IS_WRONG_TYPE.format(
                 config_var="DATABASE_NAME",
                 config_var_type = "string",
                 config_incorrect_type = type(DATABASE_NAME).__name__
             )
        )

    # DATABASE_HOST
    DATABASE_HOST = app.config.get("DATABASE_HOST")
    if DATABASE_HOST is None:
        environ_var = os.environ.get("EVALHALLA_DATABASE_HOST")
        if environ_var is None:
            raise ValueError(
                CONFIG_VAR_DOES_NOT_EXIST.format(
                    config_var = "DATABASE_HOST"
                )
            )
        else:
            app.config["DATABASE_HOST"] = environ_var
    elif not isinstance(DATABASE_HOST, str):
        raise TypeError(
            CONFIG_IS_WRONG_TYPE.format(
                config_var = "DATABASE_HOST",
                config_var_type = "string",
                config_incorrect_type = type(DATABASE_HOST).__name__
            )
        )

    # DATABASE_PORT
    DATABASE_PORT = app.config.get("DATABASE_PORT")
    if DATABASE_PORT is None:
        environ_var = os.environ.get("EVALHALLA_DATABASE_PORT") 
        if environ_var is None:
            app.config["DATABASE_PORT"] = 5432
            logging.warn(
                "DATABASE_PORT was not set as a configuration variable or environment variable. " +
                "Defaulting to 5432 as DATABASE_PORT"    
            )
        else:
            # cast environment variable into int
            try:
                environ_var = int(environ_var) # type: ignore

            except ValueError:
                raise TypeError(
                    CONFIG_IS_WRONG_TYPE.format(
                        config_var = "DATABASE_PORT",
                        config_var_type = "integer",
                        config_incorrect_type = "string"
                    )
                )

            app.config["DATABASE_PORT"] = environ_var
    
    elif not isinstance(DATABASE_PORT, int):
        raise TypeError(
            CONFIG_IS_WRONG_TYPE.format(
                config_var = "DATABASE_PORT",
                config_var_type = "integer",
                config_incorrect_type = type(DATABASE_PORT).__name__
            )
        )
    

    #DATABASE_USER
    DATABASE_USER = app.config.get("DATABASE_USER")
    if DATABASE_USER is None:
        environ_var = os.environ.get("EVALHALLA_DATABASE_USER")
        if environ_var is None:
            raise ValueError(
                CONFIG_VAR_DOES_NOT_EXIST.format(
                    config_var = "DATABASE_USER"
                )
            )
        else:
            app.config["DATABASE_USER"] = environ_var
    elif not isinstance(DATABASE_USER, str):
        raise TypeError(
            CONFIG_IS_WRONG_TYPE.format(
                config_var = "DATABASE_USER",
                config_var_type = "string",
                config_incorrect_type = type(DATABASE_USER).__name__
            )
        )

    #DATABASE_PASSWORD
    DATABASE_PASSWORD = app.config.get("DATABASE_PASSWORD")
    if DATABASE_PASSWORD is None:
        environ_var = os.environ.get("EVALHALLA_DATABASE_PASSWORD")
        if environ_var is None:
            raise ValueError(
                CONFIG_VAR_DOES_NOT_EXIST.format(
                    config_var = "DATABASE_PASSWORD"
                )
            )
        else:
            app.config["DATABASE_PASSWORD"] = environ_var
    elif not isinstance(DATABASE_PASSWORD, str):
        raise TypeError(
            CONFIG_IS_WRONG_TYPE.format(
                config_var = "DATABASE_PASSWORD",
                config_var_type = "string",
                config_incorrect_type = type(DATABASE_PASSWORD).__name__
            )
        )

    # construct the database URI for sqlalchemy
    DATABASE_USER = app.config.get("DATABASE_USER")
    DATABASE_PASSWORD = app.config.get("DATABASE_PASSWORD")
    DATABASE_HOST = app.config.get("DATABASE_HOST")
    DATABASE_PORT = app.config.get("DATABASE_PORT")
    DATABASE_NAME = app.config.get("DATABASE_NAME")
    app.config["DATABASE_URI"] = (
        f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@" +
        f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    )

    # check if AMQP exists and construct BROKER_URI
    # it's different than database configs however, environment vars override py config files
    
    # AMQP_USER
    AMQP_USER = app.config.get("AMQP_USER")
    environ_var = os.environ.get("EVALHALLA_AMQP_USER")
    if environ_var is None and AMQP_USER is None:
        raise ValueError(
            CONFIG_VAR_DOES_NOT_EXIST.format(
                config_var = "AMQP_USER"
            )
        )
    elif environ_var is not None:
        app.config["AMQP_USER"] = environ_var
    elif not isinstance(AMQP_USER, str):
        raise TypeError(
            CONFIG_IS_WRONG_TYPE.format(
                config_var = "AMQP_USER",
                config_var_type = "string",
                config_incorrect_type = type(AMQP_USER).__name__
            )
        )
    
    # AMQP_PASSWORD
    AMQP_PASSWORD = app.config.get("AMQP_PASSWORD")
    environ_var = os.environ.get("EVALHALLA_AMQP_PASSWORD")
    if environ_var is None and AMQP_PASSWORD is None:
        raise ValueError(
            CONFIG_VAR_DOES_NOT_EXIST.format(
                config_var = "AMQP_PASSWORD"
            )
        )
    elif environ_var is not None:
        app.config["AMQP_PASSWORD"] = environ_var
    elif not isinstance(AMQP_PASSWORD, str):
        raise TypeError(
            CONFIG_IS_WRONG_TYPE.format(
                config_var = "AMQP_PASSWORD",
                config_var_type = "string",
                config_incorrect_type = type(AMQP_PASSWORD).__name__
            )
        )
    
    # AMQP_HOST
    # defaults to localhost if the config doesn't exist
    AMQP_HOST = app.config.get("AMQP_HOST")
    environ_var = os.environ.get("EVALHALLA_AMQP_HOST")
    if environ_var is None and AMQP_HOST is None:
        logging.warn(
            "config value AMQP_HOST not set, defaulting to localhost"
        )
        app.config["AMQP_HOST"] = "localhost"
    elif environ_var is not None:
        app.config["AMQP_HOST"] = AMQP_HOST
    elif not isinstance(AMQP_HOST, str):
        raise TypeError(
            CONFIG_IS_WRONG_TYPE.format(
                config_var = "AMQP_HOST",
                config_var_type = "string",
                config_incorrect_type = type(AMQP_HOST).__name__
            )
        )
    
    # AMQP_VHOST
    # defaults to evalhalla if the config doesn't exist
    AMQP_VHOST = app.config.get("AMQP_VHOST")
    environ_var = os.environ.get("EVALHALLA_AMQP_VHOST")
    if environ_var is None and AMQP_VHOST is None:
        logging.warn(
            "config value AMQP_VHOST not set, defaulting to evalhalla"
        )
    elif environ_var is not None:
        app.config["AMQP_VHOST"] = environ_var
    elif not isinstance(AMQP_VHOST, str):
        raise TypeError(
            CONFIG_IS_WRONG_TYPE.format(
                config_var = "AMQP_VHOST",
                config_var_type = "string",
                config_incorrect_type = type(AMQP_VHOST).__name__
            )
        )
    
    # AMQP_PORT
    # defaults to AMQP default port 
    AMQP_PORT = app.config.get("AMQP_PORT")
    environ_var = os.environ.get("AMQP_PORT")
    if environ_var is None and AMQP_PORT is None:
        logging.warn(
            "config value AMQP_PORT not et, defaulting to 5672"
        )
        app.config["AMQP_PORT"] = 5672
    elif environ_var is not None:
        try:
            environ_var = int(environ_var)
        except ValueError:
            raise TypeError(
                CONFIG_IS_WRONG_TYPE.format(
                    config_var="AMQP_PORT",
                    config_var_type = "integer",
                    config_incorrect_type = "string"
                )
            )
        app.config["AMQP_PORT"] = environ_var
    elif not isinstance(AMQP_PORT, int):
        raise TypeError(
            CONFIG_IS_WRONG_TYPE.format(
                config_var="AMQP_PORT",
                config_var_type = "integer",
                config_incorrect_type = "string"
            )
        )

    # construct AMQP_URI 
    AMQP_HOST = app.config.get("AMQP_HOST")
    AMQP_PORT = app.config.get("AMQP_PORT")
    AMQP_USER = app.config.get("AMQP_USER")
    AMQP_PASSWORD = app.config.get("AMQP_PASSWORD")
    AMQP_VHOST = app.config.get("AMQP_VHOST")
    app.config["BROKER_URI"] = f"amqp://{AMQP_USER}:{AMQP_PASSWORD}@{AMQP_HOST}:{AMQP_PORT}/{AMQP_VHOST}"

    
    # initialize database
    initialize_database(app)

    # register the api routes
    register_routes(app)
    
    return app



    




