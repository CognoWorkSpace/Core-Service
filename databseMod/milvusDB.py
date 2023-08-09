import numpy as np
import pandas as pd
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from towhee import ops, pipe, DataCollection
from typing import List


class MilvusDB:
    def __init__(self, host: str = '127.0.0.1', port: str = '19530'):
        self._host = host
        self._port = port
        connections.connect(host=host, port=port)

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

    @staticmethod
    def get_collection_by_name(collection_name):
        assert utility.has_collection(collection_name), f"Cannot find collection: {collection_name}"
        return Collection(collection_name)

    @classmethod
    def delete_from_collection(cls, collection_name: str, query: str):
        '''
            check milvus query rule: https://milvus.io/docs/boolean.md
        '''
        collection = cls.get_collection_by_name(collection_name)
        collection.delete(query)

    @staticmethod
    def drop_collectino_by_name(collection_name):
        if utility.has_collection(collection_name):
            utility.drop_collection(collection_name)
            print(f'drop collection {collection_name} successfully')
            return
        print(f"no collection named {collection_name}")

    def insert_dataframe_into_milvus(self, collection_name: str, df: pd.DataFrame):
        insert_pipe = (pipe.input('df')
                       .flat_map('df', 'data', lambda df: df.values.tolist())
                       .map('data', 'res', ops.ann_insert.milvus_client(host=self._host,
                                                                        port=self._port,
                                                                        collection_name=collection_name))
                       .output('res')
                       )

        insert_pipe(df)

    def search_in_milvus(self, query: str, collection_name: str, output_fields: List[str]):
        '''
            check milvus query rule: https://milvus.io/docs/boolean.md
        '''
        collection = self.get_collection_by_name(collection_name)
        all_fields = set(f.name for f in collection.schema.fields)
        assert all(field in all_fields for field in output_fields), \
            f"Invalid output_fields {output_fields}, fields in current collection is {all_fields}"
        # collection.load()

        search_pipe = (pipe.input('query')
                            .map('query', 'vec', ops.sentence_embedding.openai(model_name='text-embedding-ada-002',
                                                                               api_key="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"))
                            # .map('vec', 'vec', lambda x: x / np.linalg.norm(x, axis=0))
                            .flat_map('vec', ('id', 'score', *output_fields),
                                      ops.ann_search.milvus_client(host=self._host,
                                                                   port=self._port,
                                                                   collection_name=collection_name,
                                                                   output_fields=output_fields,
                                                                   limit=5))
                            .output('query', 'id', 'score', *output_fields)
                       )

        res = search_pipe(query)
        res_schema = res.schema
        return [[{res_schema[i]: data[i]} for i in range(len(res_schema))] for data in res.to_list()]



