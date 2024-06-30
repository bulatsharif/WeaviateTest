from typing import List, Optional, Dict, Any
from pydantic import BaseModel, RootModel


class Attributes(RootModel):
    root: Dict[str, Any]


class Ops(BaseModel):
    insert: str
    attributes: Optional[Attributes] = None


class Content(BaseModel):
    ops: List[Ops]


class SearchInput(BaseModel):
    searchString: str


class ArticleAdd(BaseModel):
    tags: List[str]
    title: str
    text: str
    content: Content


class ArticleGet(BaseModel):
    id: str
    tags: List[str]
    title: str
    text: str
    content: Content


class Question(BaseModel):
    question: str
