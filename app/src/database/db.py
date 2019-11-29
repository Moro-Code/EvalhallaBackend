from flask import Flask
import psycopg2


def check_if_db_exists_and_create(app: Flask) -> None:
    """
    Checks if the database exists, if not creates the database and the schema
    """
    db_host = app.config["DATABASE_HOST"]
    db_port = app.config["DATABASE_PORT"]
    db_user = app.config["DATABASE_USER"]
    db_password = app.config["DATABASE_PASSWORD"]
    db_name = app.config["DATABASE_NAME"]

    # connect to the database server
    connection = psycopg2.connect(
        user = db_user, host = db_host, 
        password = db_password, port = db_port
    )

    # create a cursor
    cursor = connection.cursor()

    # check if database exists
    cursor.execute(
        f"SELECT exists( SELECT datname FROM pg_catalog.pg_database WHERE datname='{db_name}' );"
    )


    exists = cursor.fetchone()[0]

    # create database if it does not exist
    if not exists:
        cursor.execute(f"CREATE DATABASE '{db_name}';")
        cursor.commit()
    
    # close the cursor and connection
    cursor.close()
    connection.close()









