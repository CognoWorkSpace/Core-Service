# The part to connect Postgres database
PGVECTOR_DRIVER = "psycopg2"
PGVECTOR_HOST = "172.28.30.52"
PGVECTOR_PORT = "5432"
PGVECTOR_DATABASE = "testdb"
PGVECTOR_USER = "test"
PGVECTOR_PASSWORD = "test"

# The part to connect Milvus database
MILVUS_HOST = ""
MILVUS_PORT = ""
MILVUS_USER = "test"
MILVUS_PASSWORD = "test"


# The part to fill openAI information
OPENAI_MODEL_NAME = "gpt-4"
OPENAI_TEMPERATURE = 0.7
OPENAI_MAX_TOKENS = 1024
OPENAI_API_KEY = "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"
BUFFER_TOP_K = 5
