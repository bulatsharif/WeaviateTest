from src.knowledge_base.models import ArticleGet, ArticleAdd, Content
from typing import List, Dict, Optional, Any
from src.weaviate_client import client
from pydantic import BaseModel
from fastapi import APIRouter
import json

router = APIRouter(
    prefix="/knowledge-base/edit",
    tags=["Knowledge Base Editor"]
)


class MarkdownContent(BaseModel):
    content: Dict[str, Any]
    tags: List[str] = []
    title: Optional[str] = None
    text: Optional[str] = None


@router.post("/create-article/", response_model=ArticleGet)
async def create_article(article: ArticleAdd):
    content_dict = article.content.dict()
    content_json = json.dumps(content_dict)
    article_object = {
        "tags": article.tags,
        "title": article.title,
        "text": article.text,
        "content": content_json
    }
    result = client.data_object.create(
        data_object=article_object,
        class_name="Article"
    )
    object_id = result

    return ArticleGet(
        id=object_id,
        tags=article.tags,
        title=article.title,
        text=article.text,
        content=article.content
    )


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
async def edit_article(article: ArticleAdd, article_id: str):
    content_dict = article.content.dict()
    content_json = json.dumps(content_dict)

    article_object = {
        "tags": article.tags,
        "title": article.title,
        "text": article.text,
        "content": content_json
    }

    client.data_object.replace(
        uuid=article_id,
        class_name="Article",
        data_object=article_object
    )

    return ArticleGet(
        id=article_id,
        tags=article.tags,
        title=article.title,
        text=article.text,
        content=article.content
    )
