import pandas as pd
from langchain.embeddings.openai import OpenAIEmbeddings


df = pd.read_csv('wineData/wine.csv', nrows=10000, index_col=0)
df.dropna(inplace=True)

df_used = df.head(1000)
df_wine = df_used[['title', 'country', 'points', 'province', 'variety', 'winery', 'price', 'description']].copy()

# print(df_wine.describe())

cols = df_wine.columns
df_wine['combined'] = \
    ['; '.join(f'{k}: {str(v).strip()}' for k, v in i.items()) for i in df_wine[cols].to_dict('records')]

print('Embedding combination info...')
embedding_model = OpenAIEmbeddings(openai_api_key="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")
df_wine['wine_info_embed'] = embedding_model.embed_documents(df_wine['combined'])

df_wine.to_csv('wineData/wine_data_w_embed.csv', index=False)
print('Write csv data successfully')