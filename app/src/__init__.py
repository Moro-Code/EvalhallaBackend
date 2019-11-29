
from flask import Flask
import os
import logging
import sys
from .database import check_if_db_exists_and_create


def create_app(env="production") -> Flask:

    app = Flask(__name__)

    # importing the default configuration
    from src.config import default
    app.config.from_object(default)

    # depending on environment load the correct configuration
    if env == "production":
        from src.config import production
        app.config.from_object(production)
    else:
        from src.config import development
        app.config.from_object(development)

        @app.route("/testing")
        def testing():
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
            "Configuration variable DATABASE_NAME must be of type string, " + 
            f"recieved {type(DATABASE_NAME).__name__}"
        )

    # DATABASE_HOST
    DATABASE_HOST = app.config.get("DATABASE_HOST")
    if DATABASE_HOST is None:
        environ_var = os.environ.get("EVALHALLA_DATABASE_HOST")
        if environ_var is None:
            raise ValueError(
                "DATABSE_HOST is a required configuration variable, " + 
                "config value and environment varliable is None"
            )
        else:
            app.config["DATABASE_HOST"] = environ_var
    elif not isinstance(DATABASE_HOST, str):
        raise TypeError(
            "Configuration variable DATABASE_NAME must be of type string, " + 
            f"recieved {type(DATABASE_HOST).__name__}"
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

            except ValueError as e:
                raise ValueError("DATABSE_PORT must be a valid number")

            app.config["DATABASE_PORT"] = environ_var
    
    elif not isinstance(DATABASE_PORT, int):
        raise TypeError(
            "Configuration variable DATABASE_PORT must be of type int, " + 
            f"recieved {type(DATABASE_PORT).__name__}"
        )
    

    #DATABASE_USER
    DATABASE_USER = app.config.get("DATABASE_USER")
    if DATABASE_USER is None:
        environ_var = os.environ.get("EVALHALLA_DATABASE_USER")
        if environ_var is None:
            raise ValueError(
                "DATABSE_HOST is a required configuration variable, " + 
                "config value and environment varliable is None"
            )
        else:
            app.config["DATABASE_USER"] = environ_var
    elif not isinstance(DATABASE_USER, str):
        raise TypeError(
            "Configuration variable DATABASE_NAME must be of type string, " + 
            f"recieved {type(DATABASE_USER).__name__}"
        )

    #DATABASE_PASSWORD
    DATABASE_PASSWORD = app.config.get("DATABASE_PASSWORD")
    if DATABASE_PASSWORD is None:
        environ_var = os.environ.get("EVALHALLA_DATABASE_PASSWORD")
        if environ_var is None:
            raise ValueError(
                "DATABSE_HOST is a required configuration variable, " + 
                "config value and environment varliable is None"
            )
        else:
            app.config["DATABASE_PASSWORD"] = environ_var
    elif not isinstance(DATABASE_PASSWORD, str):
        raise TypeError(
            "Configuration variable DATABASE_NAME must be of type string, " + 
            f"recieved {type(DATABASE_PASSWORD).__name__}"
        )

    # construct the database URI for sqlalchemy
    app.config["DATABASE_URI"] = (
        f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@" +
        f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    )

    check_if_db_exists_and_create(app)
    
    return app 



    




