from typing import List

from pydantic import BaseModel, field_validator, validator


class OrganizationAdd(BaseModel):
    name: str
    description: str
    logo_link: str
    link: str
    categories: List[str]
    countries: List[str]


class OrganizationGet(BaseModel):
    id: str
    name: str
    link: str
    description: str
    logo_link: str
    categories: List[str]
    countries: List[str]

class OrganizationSearch(BaseModel):
    categories: List[str] = []
    countries: List[str] = []

class SearchInput(BaseModel):
    searchString: str
    limitOfNews: int
