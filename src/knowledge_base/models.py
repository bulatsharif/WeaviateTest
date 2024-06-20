from typing import List

from pydantic import BaseModel


class ArticleAdd(BaseModel):
    tags: List[str]
    title: str
    text: str


class ArticleGet(BaseModel):
    id: str
    tags: List[str]
    title: str
    text: str