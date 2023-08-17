from langchain.embeddings.openai import OpenAIEmbeddings
import numpy as np
import pandas as pd
from pathlib import Path
from pymilvus import connections, db, FieldSchema, CollectionSchema, DataType, Collection, utility
# from towhee import ops, pipe, DataCollection
from typing import List, Union, Iterable, Optional

from varcharLength import VarcharLength


class MilvusDB:
    def __init__(self, host: str = '127.0.0.1', port: str = '19530'):
        self._host = host
        self._port = port
        self._db_name = 'default'
        self._collection = None
        self._vector_field_name = ''
        self._collection_loaded = False
        connections.connect(host=host, port=port)

    @property
    def db_name(self):
        return self._db_name

    @db_name.setter
    def db_name(self, database_name: str):
        if database_name not in db.list_database():
            self.create_database(database_name)
        db.using_database(database_name)
        self._db_name = database_name

    @property
    def collection(self):
        return self._collection

    @collection.setter
    def collection(self, collection: Union[str, Collection]):
        if isinstance(collection, str):
            assert utility.has_collection(collection), \
                f"Cannot find collection: {collection} in database: {self.db_name}. " \
                f"Select from current existed collections {self.list_collections()} or create one."
            self._collection = Collection(collection)
        elif isinstance(collection, Collection) and utility.has_collection(collection.name):
            self._collection = collection
        self._vector_field_name = self._find_vector_field_in_collection()
        self._collection_loaded = False

    @property
    def vector_field_name(self):
        return self._vector_field_name

    @staticmethod
    def create_database(database_name: str):
        if database_name in db.list_database():
            print(f"Database named {database_name} already exists. To use that database, set property db_name.")
            return
        db.create_database(database_name)

    def _find_vector_field_in_collection(self):
        if self._collection:
            for field in self._collection.schema.fields:
                if field.dtype == DataType.FLOAT_VECTOR:
                    return field.name

    @classmethod
    def list_database(cls):
        return db.list_database()

    @classmethod
    def create_milvus_collection(cls, collection_name, dim):
        if utility.has_collection(collection_name):
            print(f"Collection {collection_name} already exists. If new collection with current name is needed, "
                  f"consider dropping exist collection")
            return cls.get_collection_by_name(collection_name)

        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="username", dtype=DataType.VARCHAR, max_length=500),
            FieldSchema(name="rev_score", dtype=DataType.INT64),
            FieldSchema(name="review", dtype=DataType.VARCHAR, max_length=800),
            FieldSchema(name="review_embed", dtype=DataType.FLOAT_VECTOR, dim=dim)
        ]

        schema = CollectionSchema(fields=fields, description='product review')
        collection = Collection(name=collection_name, schema=schema)

        index_params = {
            'metric_type': "L2",
            'index_type': "IVF_FLAT",
            'params': {"nlist": 2048}
        }
        collection.create_index(field_name='review_embed', index_params=index_params)
        return collection

    def create_collection_by_df(self, df: pd.DataFrame, collection_name: str,
                                schema_description: str, pk_field_name: Optional[str]) -> Collection:
        '''
        Notice: Milvus ONLY support single vector field currently.
                Check pymilvus.exceptions.MilvusException:
                <MilvusException: (code=1, message=multiple vector fields is not supported>
        pk_field_name: Specify primary key field name of collection,
                       None for using auto primary key
        '''
        if utility.has_collection(collection_name):
            print(f"Collection {collection_name} already exists. If new collection with current name is needed, "
                  f"consider dropping exist collection")
            self.collection = collection_name
            return self.collection

        schema = self._create_schema_by_dataframe(df, schema_description, pk_field_name=pk_field_name)
        self.collection = Collection(name=collection_name, schema=schema)

        index_params = {
            'metric_type': "L2",
            'index_type': "IVF_FLAT",
            'params': {"nlist": 2048}
        }
        self.collection.create_index(field_name=self.vector_field_name, index_params=index_params)
        # for field in schema.fields:
        #     if field.dtype == DataType.FLOAT_VECTOR:
        #         collection.create_index(field_name=field.name, index_params=index_params)
        return self.collection

    @classmethod
    def read_df_with_vector(cls, csv_file_path: Union[str, Path], embedded_col: str,
                            index_col: Optional[Union[str, Iterable]] = None):
        df = pd.read_csv(csv_file_path,
                         converters={embedded_col: lambda x: eval(x)})
        # df = pd.read_csv(csv_file_path,
        #                  converters={col: (lambda x: eval(x)) for col in embedded_cols})
        if index_col:
            df.set_index(index_col, drop=True, inplace=True)
        return df

    @classmethod
    def _create_field_schema_by_pd_series(cls, series: pd.Series) -> FieldSchema:
        sample_data = series[0]
        if isinstance(sample_data, list):
            return FieldSchema(name=series.name, dtype=DataType.FLOAT_VECTOR, dim=len(sample_data))
        elif isinstance(sample_data, str):
            if series.str.len().max() <= (VarcharLength.Small >> 2):
                return FieldSchema(name=series.name, dtype=DataType.VARCHAR, max_length=int(VarcharLength.Small))
            elif series.str.len().max() <= (VarcharLength.Middle >> 2):
                return FieldSchema(name=series.name, dtype=DataType.VARCHAR, max_length=int(VarcharLength.Middle))
            elif series.str.len().max() <= (VarcharLength.Large >> 2):
                return FieldSchema(name=series.name, dtype=DataType.VARCHAR, max_length=int(VarcharLength.Large))
            elif series.str.len().max() <= (VarcharLength.ExLarge >> 2):
                return FieldSchema(name=series.name, dtype=DataType.VARCHAR, max_length=int(VarcharLength.ExLarge))
            else:
                return FieldSchema(name=series.name, dtype=DataType.VARCHAR, max_length=int(VarcharLength.Max))
        elif isinstance(sample_data, (int, np.integer)):
            return FieldSchema(name=series.name, dtype=DataType.INT64)
        elif isinstance(sample_data, (float, np.float)):
            return FieldSchema(name=series.name, dtype=DataType.FLOAT)
        elif isinstance(sample_data, bool):
            return FieldSchema(name=series.name, dtype=DataType.BOOL)
        else:
            print(f"unknown datatype for column {series.name}, check pymilvus DataType")
            return FieldSchema(name=series.name, dtype=DataType.UNKNOWN)

    @classmethod
    def _create_schema_by_dataframe(cls, df: pd.DataFrame, schema_description: str, pk_field_name: Optional[str]):
        fields = list()
        if not pk_field_name:
            fields.append(FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True))
        else:
            pk_field = cls._create_field_schema_by_pd_series(df[pk_field_name])
            pk_field.is_primary = True
            pk_field.auto_id = False
            fields.append(pk_field)
        fields.extend((cls._create_field_schema_by_pd_series(df[col]) for col in df.columns if col != pk_field_name))
        return CollectionSchema(fields=fields,
                                description=schema_description)

    @classmethod
    def list_collections(cls):
        return utility.list_collections()

    @classmethod
    def delete_from_collection(cls, collection_name: str, query: str):
        '''
            check milvus query rule: https://milvus.io/docs/boolean.md
        '''
        if utility.has_collection(collection_name):
            collection = Collection(collection_name)
            collection.delete(query)
            print(f"Delete data from collection {collection_name} successfully")

    @classmethod
    def drop_collection_by_name(cls, collection_name):
        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)
            print(f'drop collection {collection_name} successfully')
            return
        print(f"no collection named {collection_name}")

    def insert_df_into_collection(self, df: pd.DataFrame):
        self.collection.insert(df)
        self.collection.flush()
        print(f"Insert dataframe into collection {self.collection.name} successfully")

    def conduct_vector_similar_search(self, query: str, limit: int,
                                      output_fields: Optional[List[str]] = None,
                                      metric_type: str = "L2", nprobe: int = 10, **kwargs):
        '''
            check milvus query rule: https://milvus.io/docs/boolean.md
        '''
        assert isinstance(self.collection, Collection), "current collection is None, set to correct one"
        # all_fields = set(f.name for f in self.collection.schema.fields)
        # assert all(field in all_fields for field in output_fields), \
        #     f"Invalid output_fields {output_fields}, fields in current collection is {all_fields}"
        if not self._collection_loaded:
            self.collection.load()
            self._collection_loaded = True
        search_params = {"metric_type": metric_type, "params": {"nprobe": nprobe}}
        return self.collection.search([self.embedding_query(query)],
                                      anns_field=self.vector_field_name, param=search_params,
                                      limit=limit, output_fields=output_fields, **kwargs)

    def query_search(self, expr: str, output_fields: Optional[List[str]] = None, **kwargs):
        assert isinstance(self.collection, Collection), "current collection is None, set to correct one"
        if not self._collection_loaded:
            self.collection.load()
            self._collection_loaded = True
        return self.collection.query(expr=expr, output_fields=output_fields, **kwargs)

    @classmethod
    def embedding_query(cls, query: str,
                        model: OpenAIEmbeddings =
                        OpenAIEmbeddings(openai_api_key="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")):
        return model.embed_query(query)

    # def insert_dataframe_into_milvus(self, collection_name: str, df: pd.DataFrame):
    #     insert_pipe = (pipe.input('df')
    #                    .flat_map('df', 'data', lambda df: df.values.tolist())
    #                    .map('data', 'res', ops.ann_insert.milvus_client(host=self._host,
    #                                                                     port=self._port,
    #                                                                     db_name=self.db_name,
    #                                                                     collection_name=collection_name))
    #                    .output('res')
    #                    )
    #
    #     insert_pipe(df)
    #
    # def search_in_milvus(self, query: str, collection_name: str, output_fields: List[str]):
    #     '''
    #         check milvus query rule: https://milvus.io/docs/boolean.md
    #     '''
    #     collection = self.get_collection_by_name(collection_name)
    #     all_fields = set(f.name for f in collection.schema.fields)
    #     assert all(field in all_fields for field in output_fields), \
    #         f"Invalid output_fields {output_fields}, fields in current collection is {all_fields}"
    #     # collection.load()
    #
    #     search_pipe = (pipe.input('query')
    #                         .map('query', 'vec', ops.sentence_embedding.openai(model_name='text-embedding-ada-002',
    #                                                                            api_key="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"))
    #                         # .map('vec', 'vec', lambda x: x / np.linalg.norm(x, axis=0))
    #                         .flat_map('vec', ('id', 'score', *output_fields),
    #                                   ops.ann_search.milvus_client(host=self._host,
    #                                                                port=self._port,
    #                                                                collection_name=collection_name,
    #                                                                output_fields=output_fields,
    #                                                                limit=5))
    #                         .output('query', 'id', 'score', *output_fields)
    #                    )
    #
    #     res = search_pipe(query)
    #     res_schema = res.schema
    #     return [[{res_schema[i]: data[i]} for i in range(len(res_schema))] for data in res.to_list()]

