import os

from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from werkzeug.utils import secure_filename

import config
from modules.factories.connection_string_factory import create_connection_string
from modules.factories.database_factory import create_database
from modules.factories.embedding_factory import create_embedding


def upload(file, collection_name):
    try:

        filename = secure_filename(file.filename)
        file_path = './tmp/' + filename
        file.save(file_path)

        file_extension = os.path.splitext(
            file_path)[1][1:]  # get the file_extension

        text_splitter = RecursiveCharacterTextSplitter(
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

        embeddings = create_embedding("OpenAI")  # Creating embedding method
        connection_string = create_connection_string(
            "milvus")  # Creating Milvus connection string

        # Creating Milvus Database
        database = create_database(config.DATABASE, collection_name=collection_name,
                                   connection_string=connection_string, embeddings=embeddings)

        page_contents = [doc.page_content for doc in docs]
        metadata = [doc.metadata for doc in docs]

        database.add_texts(texts=page_contents, metadatas=metadata)

        # Deleting the file in tmp, since it already exist in Database
        if os.path.isfile(file_path):
            os.remove(file_path)
        return {"result": "success"}

    except ValueError as e:
        raise Exception(e)
