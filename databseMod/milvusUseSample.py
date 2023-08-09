import pandas as pd

from databseMod.milvusDB import MilvusDB


mvs_db = MilvusDB()

df = pd.read_csv("cognoSampleData/embeddedData/embedded_Apple_product5.csv",
                 converters={'review_embed': lambda x: eval(x)})
embed_dim = len(df.head(1)['review_embed'][0])
collection = mvs_db.create_milvus_collection('cogno_product_review_sample', embed_dim)

mvs_db.insert_dataframe_into_milvus(collection_name='cogno_product_review_sample',
                                    df=df)

res = mvs_db.search_in_milvus(query="音质很棒没有杂音舒适度",
                              collection_name="cogno_product_review_sample",
                              output_fields=['rev_score', 'review'])
for search_res in res:
    print(search_res)