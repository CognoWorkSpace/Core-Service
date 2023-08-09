import pandas as pd
from pathlib import Path
from langchain.embeddings.openai import OpenAIEmbeddings


def preprocess_product_review_data(csv_file: str):
    df = pd.read_csv('cognoSampleData/Apple/product1.csv', skiprows=1)
    df.rename(columns={"用户名": "username", "评分": "rev_score", "评论": "review"}, inplace=True)
    df['rev_score'] = df['rev_score'].apply(lambda x: int(x[-1]))

    model = OpenAIEmbeddings(openai_api_key="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")

    df['review_embed'] = model.embed_documents(df['review'])
    return df


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)

    origin_data = 'cognoSampleData/Apple/product5.csv'
    save_dir = Path('cognoSampleData/embeddedData')
    save_dir.mkdir(parents=True, exist_ok=True)
    df = preprocess_product_review_data(origin_data)
    print(f"processed data sample: \n{df.head(5)}")

    source_data_path_parts = origin_data.split('/')
    save_path = save_dir / f'embedded_{source_data_path_parts[-2]}_{source_data_path_parts[-1]}'
    df.to_csv(save_path, index=False)
    print(f'\nsave processed data to {save_path} successfully')

