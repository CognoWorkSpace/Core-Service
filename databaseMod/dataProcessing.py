from concurrent.futures import ProcessPoolExecutor
from itertools import repeat
import glob
import pandas as pd
from pathlib import Path
from langchain.embeddings.openai import OpenAIEmbeddings


def preprocess_product_review_data(csv_file: str, embedding_model, write_dir: Path = None):

    assert write_dir is None or write_dir.exists() and write_dir.is_dir(), \
        "Make sure write_dir is correct directory path to save embedded product review data"

    df_product_params = pd.read_csv(csv_file, nrows=1)
    product_link = df_product_params.columns[0]

    df = pd.read_csv(csv_file, skiprows=1)
    df.rename(columns={"用户名": "username", "评分": "rev_score", "评论": "review"}, inplace=True)
    df['rev_score'] = df['rev_score'].apply(lambda x: int(x[-1]))
    df['product_link'] = product_link

    df['review_embed'] = embedding_model.embed_documents(df['review'])

    if write_dir:
        source_data_path_parts = csv_file.split('/')
        write_data_path = write_dir / f'product_review_{source_data_path_parts[-2]}_{source_data_path_parts[-1]}'
        df.to_csv(write_data_path, index=False)
    return df


def preprocessing_product_params_data(product_params_csv, embedding_model, write_dir: Path):
    df = pd.read_csv(product_params_csv, skiprows=1,
                     usecols=['购买链接', '产品名称.1', '产品简介', '产品详情'])
    df.rename(columns={'购买链接': 'product_link', '产品名称.1': 'product_name',
                       '产品简介': 'product_intro', '产品详情': 'description'},
              inplace=True)

    df.dropna(subset=['product_name'], inplace=True)
    df.fillna(method='ffill', axis=1, inplace=True)

    # milvus db only support one vector field in a schema
    embed_fields = ['product_intro']
    for field in embed_fields:
        df[f"{field}_embed"] = embedding_model.embed_documents(df[field])

    if write_dir:
        df.to_csv(write_dir / 'product_data.csv', index=False)

    return df


def process_review_data_by_dir(review_data_dir_path: Path, embedding_model, write_dir: Path):
    assert review_data_dir_path.exists() and review_data_dir_path.is_dir(), \
        f"Check if dir_path {review_data_dir_path} is correct directory"
    review_data_paths = glob.iglob((review_data_dir_path / '*.csv').as_posix())
    # for path in review_data_paths:
    #     print(path)
    with ProcessPoolExecutor(max_workers=4) as executor:
        executor.map(preprocess_product_review_data, review_data_paths, repeat(embedding_model), repeat(write_dir))


if __name__ == '__main__':

    model = OpenAIEmbeddings(openai_api_key="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")

    embedded_data_save_dir = Path('cognoSampleData/embeddedData')
    process_review_data_by_dir(review_data_dir_path=Path('cognoSampleData/JDFresh'),
                               embedding_model=model,
                               write_dir=embedded_data_save_dir)

    preprocessing_product_params_data('cognoSampleData/Cogno Demo数据Sample-生鲜 - Sheet1.csv',
                                      embedding_model=model,
                                      write_dir=embedded_data_save_dir)

