from typing import List, Dict

import weaviate
from fastapi import APIRouter

from src.knowledge_base.models import ArticleGet, ArticleAdd

router = APIRouter(
    prefix="/knowledge-base/edit",
    tags=["Knowledge Base Editor"]
)

client = weaviate.Client(
    url="http://weaviate:8080",
    additional_headers = {
        "X-Jinaai-Api-Key": "jina_5d1f8bfbfcb64374b320054c5627291dy0Ph73OTluT40uUOOVb4vn7cAPAr",
        "X-Mistral-Api-Key": "RVBRn5Sn26ONsd0CbFBjYWJYR9w416kd"
    }
)



@router.post("/create-article/", response_model=ArticleGet)
async def create_article(article: ArticleAdd):
    article_object = {
        "tags": article.tags,
        "title": article.title,
        "text": article.text
    }

    result = client.data_object.create(
        data_object=article_object,
        class_name="Article"
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