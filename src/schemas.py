class_article = {
    "class": "Article",
    "properties": [
        {
            "name": "tags",
            "dataType": ["text[]"]
        },
        {
            "name": "title",
            "dataType": ["text"]
        },
        {
            "name": "text",
            "dataType": ["text"]
        },
        {
            "name": "content",
            "dataType": ["text"],
            "vectorizer": "none"
        }
    ],
    "moduleConfig": {
        "generative-mistral": {
            "model": "mistral-medium-latest",
        },
    }
}

class_saved_article = {
    "class": "ArticleSaved",
    "properties": [
        {
            "name": "tags",
            "dataType": ["text[]"]
        },
        {
            "name": "title",
            "dataType": ["text"]
        },
        {
            "name": "text",
            "dataType": ["text"]
        },
        {
            "name": "content",
            "dataType": ["text"],
            "vectorizer": "none"
        }
    ],
    "vectorizer": "none"
}

class_organization = {
    "class": "Organization",
    "properties": [
        {
            "name": "name",
            "dataType": ["text"]
        },
        {
            "name": "description",
            "dataType": ["text"]
        },
        {
            "name": "link",
            "dataType": ["text"]
        },
        {
            "name": "categories",
            "dataType": ["text[]"]
        },
        {
            "name": "countries",
            "dataType": ["text[]"]
        },
    ],
    "vectorizer": "none"
}

class_saved_organization = {
    "class": "OrganizationSaved",
    "properties": [
        {
            "name": "name",
            "dataType": ["text"]
        },
        {
            "name": "description",
            "dataType": ["text"]
        },
        {
            "name": "link",
            "dataType": ["text"]
        },
        {
            "name": "categories",
            "dataType": ["text[]"]
        },
        {
            "name": "countries",
            "dataType": ["text[]"]
        },
    ],
    "vectorizer": "none"
}

class_news = {
    "class": "News",
    "properties": [
        {
            "name": "name",
            "dataType": ["text"]
        },
        {
            "name": "body",
            "dataType": ["text"]
        },
        {
            "name": "source_link",
            "dataType": ["text"]
        },
        {
            "name": "tags",
            "dataType": ["text[]"]
        }
    ],
    "vectorizer": "none"
}

class_saved_news = {
    "class": "SavedNews",
    "properties": [
        {
            "name": "name",
            "dataType": ["text"]
        },
        {
            "name": "body",
            "dataType": ["text"]
        },
        {
            "name": "source_link",
            "dataType": ["text"]
        },
        {
            "name": "tags",
            "dataType": ["text[]"]
        }
    ],
    "vectorizer": "none"
}

class_requests = {
    "class": "Request",
    "properties": [
        {
            "name": "requestText",
            "dataType": ["text"]
        }
    ],
    "vectorizer": "none"
}