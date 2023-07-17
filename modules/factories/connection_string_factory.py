from langchain.vectorstores.pgvector import PGVector

from util import conf

import const


def create_connection_string(database_name="", **kwargs):
    if database_name == const.POSTGRES:  # if the required database is postgres, return the connection string
        if 'pgvector_driver' not in kwargs:
            kwargs['pgvector_driver'] = conf().get(key="PGVECTOR_DRIVER", default="")

        if 'pgvector_host' not in kwargs:
            kwargs['pgvector_host'] = conf().get(key="PGVECTOR_HOST", default="")

        if 'pgvector_port' not in kwargs:
            kwargs['pgvector_port'] = conf().get(key="PGVECTOR_PORT", default="")

        if 'pgvector_database' not in kwargs:
            kwargs['pgvector_database'] = conf().get(key="PGVECTOR_DATABASE", default="")

        if 'pgvector_user' not in kwargs:
            kwargs['pgvector_user'] = conf().get(key="PGVECTOR_USER", default="")

        if 'pgvector_password' not in kwargs:
            kwargs['pgvector_password'] = conf().get(key="PGVECTOR_PASSWORD", default="")

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
            kwargs['milvus_host'] = conf().get(key="MILVUS_HOST", default="")

        if 'milvus_port' not in kwargs:
            kwargs['milvus_port'] = conf().get(key="MILVUS_PORT", default="")

        if 'milvus_user' not in kwargs:
            kwargs['milvus_user'] = conf().get(key="MILVUS_USER", default="")

        if 'milvus_password' not in kwargs:
            kwargs['milvus_password'] = conf().get(key="MILVUS_PASSWORD", default="")

        connection_args = {"host": kwargs['milvus_host'], "port": kwargs['milvus_port'],
                           "user": kwargs['milvus_user'], "password": kwargs['milvus_password']}
        return connection_args

    else:
        raise ValueError("Database does not exist!")
