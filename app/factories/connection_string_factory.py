import config
from langchain.vectorstores.pgvector import PGVector


def create_connection_string(database_name="postgres", **kwargs):

    if 'pgvector_driver' not in kwargs:
        kwargs['pgvector_driver'] = config.PGVECTOR_DRIVER

    if 'pgvector_host' not in kwargs:
        kwargs['pgvector_host'] = config.PGVECTOR_HOST

    if 'pgvector_port' not in kwargs:
        kwargs['pgvector_port'] = config.PGVECTOR_PORT

    if 'pgvector_database' not in kwargs:
        kwargs['pgvector_database'] = config.PGVECTOR_DATABASE

    if 'pgvector_user' not in kwargs:
        kwargs['pgvector_user'] = config.PGVECTOR_USER

    if 'pgvector_password' not in kwargs:
        kwargs['pgvector_password'] = config.PGVECTOR_PASSWORD

    if database_name == "postgres":
        return PGVector.connection_string_from_db_params(
            driver=kwargs['pgvector_driver'],
            host=kwargs['pgvector_host'],
            port=int(kwargs['pgvector_port']),
            database=kwargs['pgvector_database'],
            user=kwargs['pgvector_user'],
            password=kwargs['pgvector_password'],
        )
    else:
        raise ValueError("Database does not exist!")
