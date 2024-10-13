# **Core-Service**

## Introduction

This is a core server based on LangChain, designed to connect SQL and Milvus databases, retrieve user information, search databases, and call large language models. The project is built on the Flask framework, with plans to support logging (to be completed), and future integration of Agent functionality.

## Installation

After cloning this repository, you need to configure the config and environment variables, then deploy using Docker Compose.

### Configuring config

Navigate to the config directory and choose the config you want to use. For testing purposes, it's recommended to use `config_test.yml`.

### Configuring the environment

Copy `.env_copy` to `.env`, fill in the `OPENAI_API_KEY`, and set `FLASK_ENV=` to the environment corresponding to your chosen config: test, dev, or pro.

### Docker Compose Installation

Check if Docker Compose is installed in your environment:
```bash
docker compose version
```

If not, download and install Docker Compose. Here's the installation method for Ubuntu:
```bash
sudo apt-get update
sudo apt-get install docker-compose-plugin
```

For other environments, please refer to the detailed tutorial in the [docker-compose official documentation](https://docs.docker.com/compose/install/linux/)

### Running the Docker environment
Run the sh script directly:
```bash
sudo ./build.sh
```
Or run:
```bash
docker-compose build
docker-compose up
```

## Task Progress

- [x] Normal conversation
  - [x] Ordinary dialogue
  - [x] Multi-turn dialogue
- [ ] Add prompts
- [ ] Add sensitive words
- [x] Discuss Agent issues
- [x] Add logging
- [x] Milvus database upload **This feature is not final, to be improved**
  - [ ] TXT
  - [ ] PDF
  - [ ] CSV
- [ ] Connect to MySQL database
- [x] Milvus database testing **This feature is not final, to be improved**
  - [x] Support multi-turn search
- [ ] Call search engine for queries
- [x] Three different Splitter methods (to be tested)
- [x] Update util
- [x] Restructure config
- [x] Docker deployment
- [x] AWS testing

## APIs

### Chat API

Endpoint:  
**POST /chat**

Description:
This API endpoint supports conversations with the AI model. It accepts a JSON payload with conversation history, a query to be asked, and other details. It returns the AI's reply (string) and the updated conversation history.

Request Body:

The API expects a JSON object in the HTTP request body with the following properties:

- query (string, required): The message or question to send to the AI.

- model_name (string, optional): The name of the AI model to use for generating the reply, e.g., "OpenAI".

- history (array, optional): An array of conversation history objects. Each object has a type property, which can be "human" or "ai", and a data property containing another object with a content property that includes the message text. If this property is not provided or is an empty array, the conversation is assumed to start from the beginning. For example:

```json
{
  "history": [
    {
      "type": "human",
      "data": {
        "content": "What's your name?"
      }
    },
    {
      "type": "ai",
      "data": {
        "content": "I'm an AI model developed by OpenAI."
      }
    }
  ]
}
```

- with_memory (boolean, optional): Whether to consider the conversation history when generating the reply. If not provided, defaults to false.

Response:
The API returns a JSON object with the following properties:

- reply (string): The AI's response to the query.
- history (array): The updated array of conversation history objects, including the latest query and reply.

Example:
Here's an example request:

```json
{
  "query": "How's the weather today?",
  "model_name": "OpenAI",
  "history": [
    {
      "type": "human",
      "data": {
        "content": "What's your name?"
      }
    },
    {
      "type": "ai",
      "data": {
        "content": "I'm an AI model developed by OpenAI."
      }
    }
  ],
  "with_memory": true
}
```

And an example response:

```json
{
  "reply": "I'm sorry, as an AI, I don't have real-time capabilities to provide current weather information.",
  "history": [
    {
      "type": "human",
      "data": {
        "content": "What's your name?"
      }
    },
    {
      "type": "ai",
      "data": {
        "content": "I'm an AI model developed by OpenAI."
      }
    },
    {
      "type": "human",
      "data": {
        "content": "How's the weather today?"
      }
    },
    {
      "type": "ai",
      "data": {
        "content": "I'm sorry, as an AI, I don't have real-time capabilities to provide current weather information."
      }
    }
  ]
}
```

### Query View API

Endpoint:  
**POST /query**

Description:  
This API endpoint is used to handle and respond to interaction requests with the AI conversation system. It accepts a JSON payload with a query to be asked, the AI model name, conversation history, memory switch, database switch, and collection name. It returns either the AI's reply or error information.

When with_database is true, the system will call the search function. This function will search in the specified collection in the Milvus database and generate a response. In this case, the collection_name is required. When with_database is false, the system will simply conduct a conversation without involving database search.

Request Body:

The API expects a JSON object in the HTTP request body with the following properties:

- query (string, required): The message or question to send to the AI.

- model_name (string, optional): The name of the AI model to use for generating the reply, e.g., "OpenAI".

- history (array, optional): An array of conversation history objects, refer to the history array format mentioned above.

- with_memory (boolean, optional): Whether to consider the conversation history when generating the reply. If not provided, defaults to false.

- with_database (boolean, optional): Whether to search the corresponding collection in the database to generate the reply. If not provided, defaults to false.

- collection_name (string, optional): If using the database, this is the name of the collection to query.

Errors:  
If an error occurs, the API will return a JSON object containing the error information.

Example:  
Here's an example request:

```json
{
  "query": "How's the weather today?",
  "model_name": "OpenAI",
  "history": [
    {
      "type": "human",
      "data": {
        "content": "What's your name?"
      }
    },
    {
      "type": "ai",
      "data": {
        "content": "I'm an AI model developed by OpenAI."
      }
    }
  ],
  "with_memory": true,
  "with_database": true,
  "collection_name": "weather_collection"
}
```

Example of a successful response:

```json
{
  "reply": "Today's weather is sunny with a temperature of about 27 degrees Celsius.",
  "history": [
    {
      "type": "human",
      "data": {
        "content": "What's your name?"
      }
    },
    {
      "type": "ai",
      "data": {
        "content": "I'm an AI model developed by OpenAI."
      }
    },
    {
      "type": "human",
      "data": {
        "content": "How's the weather today?"
      }
    },
    {
      "type": "ai",
      "data": {
        "content": "Today's weather is sunny with a temperature of about 27 degrees Celsius."
      }
    }
  ]
}
```

Example of an error response:

```json
{
  "error": "Collection named 'weather_collection' not found in the database."
}
```

### File Upload API

Endpoint:  
**POST /upload**

Description:

This API endpoint supports file uploads. It receives a POST request with a file and collection name. The file is sent from the frontend using formData. The return result is in JSON format, indicating the status and related information of the upload result.

Request Body:
The API expects to receive the following parameters in the HTTP POST request:

- file (file, required): The file to be uploaded.
- collection_name (string, required): The name of the collection where the file needs to be uploaded.

Response:
The API returns a JSON object containing the following properties:

- result (string): The result status of the upload operation, e.g., "success".

- message (string, optional): Additional message about the upload result, such as error information if the upload fails. This field may not appear when the result is "success".

- error (string, optional): If an error occurs during the upload process, this field will contain the error message.

Example:
Here's a possible response example:

```json
{
  "result": "success"
}
```

And an example of a response when an error occurs:

```json
{
  "error": "File size exceeds the limit"
}
```
