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
    "下面是我们的问题: {question}\n"
    "我们已经有了一个还不成熟的答案: {existing_answer}\n"
    "如果有必要，我们需要用新的信息来生成一个更好的答案"
    "下面是新的信息\n"
    "------------\n"
    "{context_str}\n"
    "------------\n"
    "根据新的信息，改善原本的答案，让他变得更好。保证回答完全基于所提供的信息，不能自己编造信息。"
    "如果新的答案没有比旧答案好，请你直接回复旧答案，请用中文回复，麻烦您了！"
)
refine_prompt = PromptTemplate(
    input_variables=["question", "existing_answer", "context_str"],
    template=refine_prompt_template,
)


initial_qa_template = (
    "现在下面有一些关于中国宪法的信息。随后你将遇到一个问题，请你如实回答。保证回答完全基于所提供的信息。 \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "请你回答这个问题{question}\n请你使用中文回答，谢谢您！\n"
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
    collection_name="constitution",
    distance_strategy=DistanceStrategy.COSINE,
    pre_delete_collection=False,
    connection_string=CONNECTION_STRING,
)


qa_chain = load_qa_chain(OpenAI(model_name="gpt-3.5-turbo"), chain_type="refine", return_refine_steps=False,
                         question_prompt=initial_qa_prompt, refine_prompt=refine_prompt)

qa = RetrievalQA(combine_documents_chain=qa_chain,
                 retriever=vectordb.as_retriever())


def rquery(input):
    print(input)
    output = qa.run(input)
    print(output)
    return output
