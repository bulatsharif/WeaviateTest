from src.knowledge_base.knowledge_base_user.router import router as router_user
from src.knowledge_base.knowledge_base_editor.router import router as router_editor
from src.calculator.router import router as router_calculator
from src.funds.funds_user.router import router as router_funds_user
from src.funds.funds_editor.router import router as router_funds_editor
from src.QnA.QnA_user.router import router as router_qna_user
from src.QnA.QnA_editor.router import router as router_qna_editor
from src.organizations.organization_user.router import router as router_organization_user
from src.organizations.organizations_editor.router import router as router_organizations_editor
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(router_user)
app.include_router(router_editor)
app.include_router(router_calculator)
app.include_router(router_funds_user)
app.include_router(router_funds_editor)
app.include_router(router_qna_user)
app.include_router(router_qna_editor)
app.include_router(router_organization_user)
app.include_router(router_organizations_editor)
