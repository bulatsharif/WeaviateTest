from typing import List
from pydantic import BaseModel


class NewsAdd(BaseModel):
    name: str
    body: str
    image_link: str
    source_link: str
    tags: List[str]


class NewsGet(BaseModel):
    id: str
    name: str
    body: str
    image_link: str
    source_link: str
    tags: List[str]


class SearchInput(BaseModel):
    searchString: str
    limitOfNews: int



