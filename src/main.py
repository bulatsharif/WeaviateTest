from fastapi import FastAPI
import weaviate

from src.schemas import class_article, class_fund, class_question
from src.knowledge_base.knowledge_base_user.router import router as router_user
from src.knowledge_base.knowledge_base_editor.router import router as router_editor
from src.calculator.router import router as router_calculator
from src.funds.funds_user.router import router as router_funds_user
from src.funds.funds_editor.router import router as router_funds_editor
from src.QnA.QnA_user.router import router as router_qna_user
from src.QnA.QnA_editor.router import router as router_qna_editor
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

client = weaviate.Client(
    url="http://weaviate:8080",
    additional_headers = {
        "X-Jinaai-Api-Key": "jina_5d1f8bfbfcb64374b320054c5627291dy0Ph73OTluT40uUOOVb4vn7cAPAr",
        "X-Mistral-Api-Key": "RVBRn5Sn26ONsd0CbFBjYWJYR9w416kd"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if not client.schema.exists("Article"):
    client.schema.create_class(class_article)

if not client.schema.exists("Fund"):
    client.schema.create_class(class_fund)

if not client.schema.exists("Question"):
    client.schema.create_class(class_question)

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

