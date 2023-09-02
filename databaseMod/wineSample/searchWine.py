from databaseMod.milvusDB import MilvusDB


mvs_db = MilvusDB()
mvs_db.db_name = 'wine'
mvs_db.collection = 'wine_data'

print(f"Number of data in collection {mvs_db.collection.name} is {mvs_db.collection.num_entities}")

output_fields = [field.name for field in mvs_db.collection.schema.fields if field.name not in {'id', 'wine_info_embed'}]

res = mvs_db.conduct_vector_similar_search(query="sweet red wine with price under 50", limit=5,
                                           output_fields=output_fields)
for search_res in res:
    for hit in search_res:
        print(hit)

