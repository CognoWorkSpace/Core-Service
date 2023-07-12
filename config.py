import yaml

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

# General configuration
MODEL = config['model']
DATABASE = config['database']

# PostgreSQL configuration
PGVECTOR_DRIVER = config['pgvector']['driver']
PGVECTOR_HOST = config['pgvector']['host']
PGVECTOR_PORT = config['pgvector']['port']
PGVECTOR_DATABASE = config['pgvector']['database']
PGVECTOR_USER = config['pgvector']['user']
PGVECTOR_PASSWORD = config['pgvector']['password']

# Milvus configuration
MILVUS_HOST = config['milvus']['host']
MILVUS_PORT = config['milvus']['port']
MILVUS_USER = config['milvus']['user']
MILVUS_PASSWORD = config['milvus']['password']

# OpenAI configuration
OPENAI_MODEL_NAME = config['openai']['model_name']
OPENAI_TEMPERATURE = config['openai']['temperature']
OPENAI_MAX_TOKENS = config['openai']['max_tokens']
BUFFER_TOP_K = config['openai']['buffer_top_k']
