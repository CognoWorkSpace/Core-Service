from ..factories.connection_string_factory import create_connection_string
from ..factories.embedding_factory import create_embedding
from ..factories.database_factory import create_database
import config
import os

from langchain.vectorstores.pgvector import PGVector
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def upload(upload_file, collection_name):

    file_path = './tmp/' + upload_file.name
    try:
        # Files in Django will be splited into multiple chunk, we shall merge them together
        with open(file_path, 'wb+') as destination:
            for chunk in upload_file.chunks():
                destination.write(chunk)
        print(file_path)
        file_extension = os.path.splitext(
            file_path)[1][1:]  # get the file_extension

        text_splitter = RecursiveCharacterTextSplitter(
            # Set a really small chunk size, just to show.
            chunk_size=1024,
            chunk_overlap=100,
            length_function=len,
        )

        if file_extension == "csv":
            loader = CSVLoader(file_path=file_path)
            # return a list of Document Objects
            docs = loader.load_and_split(text_splitter=text_splitter)

        elif file_extension == "pdf":
            loader = PyPDFLoader(file_path=file_path)
            # return a list of Document Objects
            docs = loader.load_and_split(text_splitter=text_splitter)

        elif file_extension == "txt":
            loader = TextLoader(file_path=file_path)
            # return a list of Document Objects
            docs = loader.load_and_split(text_splitter=text_splitter)
        else:
            raise ValueError("Can't support " +
                             file_extension + " type, I'm sorry.")
    except ValueError as e:
        print(f"An error occurred: {str(e)}")

    embeddings = create_embedding("OpenAI")  # Creating embedding method
    connection_string = create_connection_string(
        "milvus")  # Creating Milvus connection string

    # Creating Milvus Database
    database = create_database("milvus", collection_name=collection_name,
                               connection_string=connection_string, embeddings=embeddings)

    page_contents = [doc.page_content for doc in docs]
    metadatas = [doc.metadata for doc in docs]

    database.add_texts(texts=page_contents, metadatas=metadatas)

    # Deleting the file in tmp, since it already exist in Database
    if os.path.isfile(file_path):
        os.remove(file_path)

    return {"result": "success"}
