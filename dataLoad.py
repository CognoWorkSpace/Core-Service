import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.vectorstores.pgvector import PGVector
from langchain.docstore.document import Document
from typing import List, Tuple
from dotenv import load_dotenv
from langchain.vectorstores.pgvector import DistanceStrategy

os.environ["OPENAI_API_KEY"] = "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"
load_dotenv()

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
    host=os.environ.get("PGVECTOR_HOST", "172.28.30.52"),
    port=int(os.environ.get("PGVECTOR_PORT", "5432")),
    database=os.environ.get("PGVECTOR_DATABASE", "testdb"),
    user=os.environ.get("PGVECTOR_USER", "test"),
    password=os.environ.get("PGVECTOR_PASSWORD", "test"),
)

loader = TextLoader('./docs/1.txt')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
data = docs
api_key = os.environ["OPENAI_API_KEY"]
embeddings = OpenAIEmbeddings()
connection_string = CONNECTION_STRING


# 上传
db = PGVector.from_documents(
    documents=docs,
    embedding=embeddings,
    collection_name="constitution",
    connection_string=connection_string,
    distance_strategy=DistanceStrategy.COSINE,
    openai_api_key=api_key,
    pre_delete_collection=False,
)


# 下载
db1 = PGVector.from_existing_index(
    embedding=embeddings,
    collection_name="constitution",
    distance_strategy=DistanceStrategy.COSINE,
    pre_delete_collection=False,
    connection_string=CONNECTION_STRING,
)

query = "国务院组成"
docs_with_score: List[Tuple[Document, float]
                      ] = db1.similarity_search_with_score(query)

for doc, score in docs_with_score:
    print("-" * 80)
    print("Score: ", score)
    print(doc.page_content)
    print("-" * 80)
