from typing import List, Dict

import ollama
from ollama import Client as ollama_client
import weaviate
from fastapi import APIRouter

from src.knowledge_base.models import ArticleGet, ArticleAdd

router = APIRouter(
    prefix="/knowledge-base/edit",
    tags=["Knowledge Base Editor"]
)

client = weaviate.Client(
    url="http://10.90.137.169:8080"
)

ollama_cl = ollama_client(host='http://host.docker.internal:11434')

@router.post("/create-article/", response_model=ArticleGet)
async def create_article(article: ArticleAdd):
    article_object = {
        "tags": article.tags,
        "title": article.title,
        "text": article.text
    }

    response = ollama_cl.embeddings(model="snowflake-arctic-embed", prompt=article_object)

    result = client.data_object.create(
        data_object=article_object,
        class_name="Article",
        vector=response["embedding"]
    )

    object_id = result

    #print(json.dumps(client.data_object.get_by_id(object_id, class_name="Article"), indent=2))

    return ArticleGet(
        id=object_id,
        tags=article.tags,
        title=article.title,
        text=article.text
    )
@router.delete("/delete-article/{article_id}", response_model=ArticleGet)
async def delete_article(article_id: str):
    article_object = client.data_object.get_by_id(
        article_id,
        class_name="Article"
    )
    client.data_object.delete(
        article_id,
        class_name="Article",
    )
    return ArticleGet(id=article_object["id"], tags=article_object["properties"]["tags"],
                      text=article_object["properties"]["text"], title=article_object["properties"]["title"])


@router.put("/edit-article/{article_id}", response_model=ArticleGet)
async def edit_article(article: ArticleAdd, article_id : str):
    article_object = {
        "tags": article.tags,
        "title": article.title,
        "text": article.text
    }

    result = client.data_object.replace(
        uuid=article_id,
        class_name="Article",
        data_object=article_object
    )

    return ArticleGet(
        id=article_id,
        tags=article.tags,
        title=article.title,
        text=article.text
    )
#@app.post("/search-article/", response_model=ArticleGet)