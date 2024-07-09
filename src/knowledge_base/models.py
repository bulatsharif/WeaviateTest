from typing import List, Optional, Dict, Any
from pydantic import BaseModel, RootModel


class Attributes(RootModel):
    root: Dict[str, Any]


class Ops(BaseModel):
    """
    Used to keep the markdown formatting within the article
    insert - the text
    attributes - formatting
    """
    insert: str
    attributes: Optional[Attributes] = None


class Content(BaseModel):
    """
    Markdown Content
    """
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


class UserRequestAdd(BaseModel):
    requestText: str


class UserRequestGet(BaseModel):
    id: str
    requestText: str


class Question(BaseModel):
    question: str



