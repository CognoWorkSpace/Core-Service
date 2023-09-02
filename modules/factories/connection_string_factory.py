from langchain.vectorstores.pgvector import PGVector

from flask import current_app

import const


def create_connection_string(database_name="", **kwargs):
    if database_name == const.POSTGRES:  # if the required database is postgres, return the connection string
        if 'pgvector_driver' not in kwargs:
            kwargs['pgvector_driver'] = current_app.config.get("PGVECTOR_DRIVER", "")

        if 'pgvector_host' not in kwargs:
            kwargs['pgvector_host'] = current_app.config.get("PGVECTOR_HOST", "")

        if 'pgvector_port' not in kwargs:
            kwargs['pgvector_port'] = current_app.config.get("PGVECTOR_PORT", "")

        if 'pgvector_database' not in kwargs:
            kwargs['pgvector_database'] = current_app.config.get("PGVECTOR_DATABASE", "")

        if 'pgvector_user' not in kwargs:
            kwargs['pgvector_user'] = current_app.config.get("PGVECTOR_USER", "")

        if 'pgvector_password' not in kwargs:
            kwargs['pgvector_password'] = current_app.config.get("PGVECTOR_PASSWORD", "")

        return PGVector.connection_string_from_db_params(
            driver=kwargs['pgvector_driver'],
            host=kwargs['pgvector_host'],
            port=int(kwargs['pgvector_port']),
            database=kwargs['pgvector_database'],
            user=kwargs['pgvector_user'],
            password=kwargs['pgvector_password'],
        )
    elif database_name == const.MILVUS:

        if 'milvus_host' not in kwargs:
            kwargs['milvus_host'] = current_app.config.get("MILVUS_HOST", "")

        if 'milvus_port' not in kwargs:
            kwargs['milvus_port'] = current_app.config.get("MILVUS_PORT", "")

        if 'milvus_user' not in kwargs:
            kwargs['milvus_user'] = current_app.config.get("MILVUS_USER", "")

        if 'milvus_password' not in kwargs:
            kwargs['milvus_password'] = current_app.config.get("MILVUS_PASSWORD", "")

        connection_args = {"host": kwargs['milvus_host'], "port": kwargs['milvus_port'],
                           "user": kwargs['milvus_user'], "password": kwargs['milvus_password']}
        return connection_args

    else:
        raise ValueError("Database does not exist!")
