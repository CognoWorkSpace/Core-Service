import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from dotenv import load_dotenv
from langchain.vectorstores.pgvector import DistanceStrategy
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain

refine_prompt_template = (
    "We now have a question about anti-money laundering laws and regulations: {question}\n"
    "We already have a structured HTML answer: {existing_answer}\n"
    "Now there is some additional information:\n"
    "------------\n"
    "{context_str}\n"
    "------------\n"
    "If the additional information is helpful to the answer, please reorganize a new answer that integrates the supplemental information, provide sources after your answers, and still needs to structure the answer and output it in HTML format, use Chinese to answer. Otherwise, just reply to the old answer."
)
refine_prompt = PromptTemplate(
    input_variables=["question", "existing_answer", "context_str"],
    template=refine_prompt_template,
)


initial_qa_template = (
    "You are now an expert in anti-money laundering laws and regulations. I will provide you with some important information from the document 'Major Laws and Regulations on Anti-Money Laundering and Counter-Terrorism Financing 2021', and then I need you to answer some questions. I hope you can structure your answers and output them in HTML format. Also, don't answer information that is not in the materials.\n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Please answer this question:{question}\n，And structure your answers, provide sources after your answers, finally output in HTML format, and answer in Chinese, thank you!\n"
)
initial_qa_prompt = PromptTemplate(
    input_variables=["context_str", "question"], template=initial_qa_template
)

os.environ["OPENAI_API_KEY"] = "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"

embeddings = OpenAIEmbeddings()

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
    host=os.environ.get("PGVECTOR_HOST", "172.28.30.52"),
    port=int(os.environ.get("PGVECTOR_PORT", "5432")),
    database=os.environ.get("PGVECTOR_DATABASE", "testdb"),
    user=os.environ.get("PGVECTOR_USER", "test"),
    password=os.environ.get("PGVECTOR_PASSWORD", "test"),
)
vectordb = PGVector.from_existing_index(
    embedding=embeddings,
    collection_name="resume",
    distance_strategy=DistanceStrategy.COSINE,
    pre_delete_collection=False,
    connection_string=CONNECTION_STRING,
)


qa_chain = load_qa_chain(OpenAI(model_name="gpt-3.5-turbo"), chain_type="refine", return_refine_steps=False,
                         question_prompt=initial_qa_prompt, refine_prompt=refine_prompt)

qa = RetrievalQA(combine_documents_chain=qa_chain,
                 retriever=vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 2}))


def queryResume(input):
    print(input)
    output = qa.run(input)
    print(output)
    return output
