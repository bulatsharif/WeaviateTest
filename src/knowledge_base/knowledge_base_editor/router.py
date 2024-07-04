from src.knowledge_base.models import ArticleGet, ArticleAdd, Content, UserRequestGet
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


def get_batch_with_cursor(collection_name, batch_size, cursor=None):
    query = (
        client.query.get(
            collection_name,
            ["requestText"]
        )
        .with_additional(["id"])
        .with_limit(batch_size)
    )
    if cursor is not None:
        result = query.with_after(cursor).do()
    else:
        result = query.do()
    return result["data"]["Get"][collection_name]


def parse_requests(data: List[Dict]) -> List[UserRequestGet]:
    requests = []
    for item in data:
        request = UserRequestGet(
            id=item['_additional']['id'],
            requestText=item['requestText']
        )
        requests.append(request)
    return requests


@router.get("/get-requests", response_model=List[UserRequestGet])
async def get_articles():
    cursor = None
    requests_unformatted = []
    while True:
        next_batch = get_batch_with_cursor("Request", 100, cursor)
        if len(next_batch) == 0:
            break
        requests_unformatted.extend(next_batch)
        cursor = next_batch[-1]["_additional"]["id"]
    requests_output = parse_requests(requests_unformatted)
    return requests_output


@router.get("/get-requests/{request_id}", response_model=UserRequestGet)
async def get_request(request_id: str):
    request_object = client.data_object.get_by_id(
        request_id,
        class_name="Request"
    )
    return UserRequestGet(id=request_object["id"], requestText=request_object["properties"]["requestText"])

@router.delete("/delete-request/{request_id}", response_model=UserRequestGet)
async def delete_request(request_id: str):
    request_object = client.data_object.get_by_id(
        request_id,
        class_name="Request"
    )
    client.data_object.delete(
        request_id,
        class_name="Request",
    )
    return UserRequestGet(id=request_object["id"], requestText=request_object["properties"]["requestText"])
