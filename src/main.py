from src.knowledge_base.knowledge_base_user.router import router as router_user
from src.knowledge_base.knowledge_base_editor.router import router as router_editor
from src.knowledge_base.knowledge_base_editor.router_saved_articles import  router as router_saved_articles
from src.calculator.router import router as router_calculator
from src.organizations.organization_user.router import router as router_organization_user
from src.organizations.organizations_editor.router import router as router_organizations_editor
from src.organizations.organizations_editor.router_saved_organization import router as router_saved_organization
from src.news.news_user.router import router as router_news_user
from src.utility.router import router as router_utility
from src.news.news_editor.router import router as router_news_editor
from src.news.news_editor.router_saved_news import router as router_saved_news
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


app = FastAPI(title="Zakat Barakat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(router_user)
app.include_router(router_editor)
app.include_router(router_saved_articles)
app.include_router(router_calculator)
app.include_router(router_organization_user)
app.include_router(router_organizations_editor)
app.include_router(router_saved_organization)
app.include_router(router_news_user)
app.include_router(router_news_editor)
app.include_router(router_saved_news)
app.include_router(router_utility)

