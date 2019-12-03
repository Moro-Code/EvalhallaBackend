from flask import Flask, current_app, g
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .models import Base


def get_db(autoflush=True, autocommit = False):
    reinitialise = False
    db_uri = current_app.config["DATABASE_URI"]
    if "db_engine" not in g:
        g.db_engine = create_engine(db_uri)
        reinitialise = True 
    if "db_factory" not in g or reinitialise:
        g.db_factory = scoped_session(
            sessionmaker(
                bind = g.db_engine, 
                autoflush=autoflush, 
                autocommit=autocommit
            )
        )
        reinitialise = True
    if "db" not in g or reinitialise:
        g.db = g.db_factory()

def close_db(e = None):
    db = g.pop("db", None)
    db_factory = g.pop("db_factoy", None)
    db_engine = g.pop("db_engine", None )

    if db is not None:
        db.close()
    if db_factory is not None:
        db_factory.remove()
    if db_engine is not None:
        db_engine.dispose()
    
def init_app(app):
    app.teardown_appcontext(close_db)
    check_if_db_exists_and_create(app)

def check_if_db_exists_and_create(app: Flask) -> None:
    """
    Checks if the database exists, if not creates the database and the schema
    """
    db_host = app.config["DATABASE_HOST"]
    db_port = app.config["DATABASE_PORT"]
    db_user = app.config["DATABASE_USER"]
    db_password = app.config["DATABASE_PASSWORD"]
    db_name = app.config["DATABASE_NAME"]
    db_uri = app.config["DATABASE_URI"]

    # connect to the database server
    connection = psycopg2.connect(
        user = db_user, host = db_host, 
        password = db_password, port = db_port
    )

    # set isolation level so that no transaction is started 
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # create a cursor
    cursor = connection.cursor()

    # check if database exists
    cursor.execute(
        f"SELECT exists( SELECT datname FROM pg_catalog.pg_database WHERE datname='{db_name}' );"
    )


    exists = cursor.fetchone()[0]

    # create database if it does not exist
    if not exists:
        cursor.execute(
            f"CREATE DATABASE {db_name};"
        )
    
    # close the cursor and connection
    cursor.close()
    connection.close()

    # create database engine 
    if not exists:
        # if db does not exist create it 
        engine = create_engine(db_uri, echo = True)
        Base.metadata.create_all(engine)
        engine.dispose()












