import pandas as pd

from databaseMod.milvusDB import MilvusDB


pd.set_option('display.max_columns', None)

mvs_db = MilvusDB()
mvs_db.db_name = 'wine'

df = mvs_db.read_df_with_vector(csv_file_path='wineData/wine_data_from_aws.csv',
                                embedded_col='wine_info_embed',
                                index_col=None)
df.drop(columns=['combined'], inplace=True)
df['points'] = df['points'].astype('int16')
df['price'] = df['price'].astype('float32')
# print(df.head())

new_collection_name = "wine_data"

mvs_db.collection = mvs_db.create_collection_by_df(
    df=df,
    collection_name=new_collection_name,
    schema_description="wine parameters data with combination embedding",
    pk_field_name=None,
)

mvs_db.insert_df_into_collection(df)

