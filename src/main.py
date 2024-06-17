import json
from typing import List, Dict
import re
from fastapi import FastAPI
import weaviate

from src.models import ArticleAdd, ArticleGet
from src.schemas import class_article, class_fund
from src.knowledge_base_user.router import router as router_user
from src.knowledge_base_editor.router import router as router_editor
from src.calculator.router import router as router_calculator
from src.funds_user.router import router as router_funds_user
from src.funds_editor.router import router as router_funds_editor
from src.QnA_user.router import router as router_qna_user
from src.QnA_editor.router import router as router_qna_editor


app = FastAPI()

client = weaviate.Client(
    url="http://10.90.137.169:8080"
)

client.schema.delete_all()

if not client.schema.exists("Article"):
    client.schema.create_class(class_article)

if not client.schema.exists("Fund"):
    client.schema.create_class(class_fund)

app.include_router(router_user)
app.include_router(router_editor)
app.include_router(router_calculator)
app.include_router(router_funds_user)
app.include_router(router_funds_editor)
app.include_router(router_qna_user)
app.include_router(router_qna_editor)

@app.get("/get-schema-meta")
async def get_schema_meta():
    print(client.schema.get("Article"))
    return client.schema.get()

