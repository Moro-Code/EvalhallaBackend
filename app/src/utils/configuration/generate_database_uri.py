

def generate_database_uri(**kwargs):
    db_name = kwargs["DATABASE_NAME"]
    db_host = kwargs["DATABASE_HOST"]
    db_port = kwargs["DATABASE_PORT"]
    db_user = kwargs["DATABASE_USER"]
    db_password = kwargs["DATABASE_PASSWORD"]
    return f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"