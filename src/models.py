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

class FundAdd(BaseModel):
    name: str
    link: str

class FundGet(BaseModel):
    id: str
    name: str
    link: str


class QuestionAdd(BaseModel):
    question: str
    answer: str
    tags: List[str]


class QuestionGet(BaseModel):
    id: str
    question: str
    answer: str
    tags: List[str]