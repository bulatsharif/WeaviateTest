class_article = {
    "class" : "Article",
    "properties": [
        {
          "name" : "tags",
          "dataType" : ["text[]"]
        },
        {
          "name" : "title",
          "dataType" : ["text"]
        },
        {
          "name" : "text",
          "dataType" : ["text"]
        },
    ],
    "vectorizer": "text2vec-ollama",
    "moduleConfig": {
        "text2vec-ollama": {
            "apiEndpoint": "http://host.docker.internal:11434",
            "model": "snowflake-arctic-embed"
        }
    },
}

class_fund = {
    "class" : "Fund",
    "properties": [
        {
          "name" : "name",
          "dataType" : ["text"]
        },
        {
          "name" : "link",
          "dataType" : ["text"]
        },
    ],
    "vectorizer": "text2vec-ollama",
    "moduleConfig": {
        "text2vec-ollama": {
            "apiEndpoint": "http://host.docker.internal:11434",
            "model": "snowflake-arctic-embed"
        }
    },
}


class_question = {
    "class" : "Question",
    "properties": [
        {
          "name" : "question",
          "dataType" : ["text"]
        },
        {
          "name" : "answer",
          "dataType" : ["text"]
        },
        {
          "name" : "tags",
          "dataType" : ["text[]"]
        },
    ],
    "vectorizer": "text2vec-ollama",
    "moduleConfig": {
        "text2vec-ollama": {
            "apiEndpoint": "http://host.docker.internal:11434",
            "model": "snowflake-arctic-embed"
        }
    },
}
