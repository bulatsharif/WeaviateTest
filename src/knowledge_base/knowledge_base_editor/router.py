import json
from typing import List, Dict, Optional, Any

import weaviate
from fastapi import APIRouter, Request
from pydantic import BaseModel

from src.knowledge_base.models import ArticleGet, ArticleAdd, Content

router = APIRouter(
    prefix="/knowledge-base/edit",
    tags=["Knowledge Base Editor"]
)

from dotenv import load_dotenv
import os

load_dotenv('.env')

jinaApi: str = os.getenv("JINA_AI_API_KEY")
mistralApi: str = os.getenv("MISTRAL_AI_API_KEY")
host: str = os.getenv("HOST")

client = weaviate.Client(
    url=host,
    additional_headers={
        "X-Jinaai-Api-Key": jinaApi,
        "X-Mistral-Api-Key": mistralApi
    }
)

class MarkdownContent(BaseModel):
    content: Dict[str, Any]  # Adjust the type based on your specific JSON structure
    tags: List[str] = []
    title: Optional[str] = None
    text: Optional[str] = None

@router.post("/create-article/", response_model=ArticleGet)
async def create_article(article: ArticleAdd):
    content_dict = article.content.dict()
    content_json = json.dumps(content_dict)

    # Create the article object
    article_object = {
        "tags": article.tags,
        "title": article.title,
        "text": article.text,
        "content": content_json
    }

    print(article_object)

    # Create the object in Weaviate
    result = client.data_object.create(
        data_object=article_object,
        class_name="Article"
    )

    # Extract the object ID from the result
    object_id = result

    # Retrieve the created object
    created_article = client.data_object.get_by_id(object_id, class_name="Article")

    print(created_article)

    # Return the ArticleGet response model
    return ArticleGet(
        id=object_id,
        tags=article.tags,
        title=article.title,
        text=article.text,
        content=article.content
    )

    # content_dict = article.content.dict()
    #
    # article_object = {
    #     "tags": article.tags,
    #     "title": article.title,
    #     "text": article.text,
    #     "content": content_dict
    # }
    #
    # print(content_dict)
    #
    # result = client.data_object.create(
    #     data_object=article_object,
    #     class_name="Article"
    # )
    #
    # object_id = result
    #
    # #print(json.dumps(client.data_object.get_by_id(object_id, class_name="Article"), indent=2))
    #
    # return ArticleGet(
    #     id=object_id,
    #     tags=article.tags,
    #     title=article.title,
    #     text=article.text,
    #     content=article.content
    # )
@router.delete("/delete-article/{article_id}", response_model=ArticleGet)
async def delete_article(article_id: str):
    article_object = client.data_object.get_by_id(
        article_id,
        class_name="Article"
    )

    content_extract = article_object["properties"]
    content = json.loads(content_extract["content"]) if 'content' in content_extract else {}
    parsed_content = Content.parse_obj(content)

    client.data_object.delete(
        article_id,
        class_name="Article",
    )
    return ArticleGet(id=article_object["id"], tags=article_object["properties"]["tags"],
                      text=article_object["properties"]["text"], title=article_object["properties"]["title"],
                      content=parsed_content)

@router.put("/edit-article/{article_id}", response_model=ArticleGet)
async def edit_article(article: ArticleAdd, article_id : str):
    content_dict = article.content.dict()
    content_json = json.dumps(content_dict)

    # Create the article object
    article_object = {
        "tags": article.tags,
        "title": article.title,
        "text": article.text,
        "content": content_json
    }


    # Create the object in Weaviate
    result = client.data_object.replace(
        uuid=article_id,
        class_name="Article",
        data_object=article_object
    )


    # Extract the object ID from the result
    # Retrieve the created object

    # Return the ArticleGet response model
    return ArticleGet(
        id=article_id,
        tags=article.tags,
        title=article.title,
        text=article.text,
        content=article.content
    )





#@app.post("/search-article/", response_model=ArticleGet)