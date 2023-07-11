import config
from langchain.vectorstores.pgvector import PGVector
from langchain.vectorstores import Milvus


def create_connection_string(database_name="postgres", **kwargs):

    if database_name == "postgres":  # if the required databse is postgres, return the connection string
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

        return PGVector.connection_string_from_db_params(
            driver=kwargs['pgvector_driver'],
            host=kwargs['pgvector_host'],
            port=int(kwargs['pgvector_port']),
            database=kwargs['pgvector_database'],
            user=kwargs['pgvector_user'],
            password=kwargs['pgvector_password'],
        )
    elif database_name == "milvus":

        if 'milvus_host' not in kwargs:
            kwargs['milvus_host'] = config.MILVUS_HOST

        if 'milvus_port' not in kwargs:
            kwargs['milvus_port'] = config.MILVUS_PORT

        if 'milvus_user' not in kwargs:
            kwargs['milvus_user'] = config.MILVUS_USER

        if 'milvus_password' not in kwargs:
            kwargs['milvus_password'] = config.MILVUS_PASSWORD

        connection_args = {"host": kwargs['milvus_host'], "port": kwargs['milvus_port'],
                           "user": kwargs['milvus_user'], "password": kwargs['milvus_password']}
        return connection_args

    else:
        raise ValueError("Database does not exist!")
