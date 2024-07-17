from dotenv import load_dotenv
import weaviate
import os

from src.schemas import class_organization, class_news, class_saved_article, class_saved_news, class_saved_organization

load_dotenv('.env')

jinaApi: str = os.getenv("JINA_AI_API_KEY")
mistralApi: str = os.getenv("MISTRAL_AI_API_KEY")
host: str = os.getenv("HOST")

client = weaviate.Client(
    url=host,
    additional_headers={
        "X-Jinaai-Api-Key": jinaApi,
        "X-Mistral-Api-Key": mistralApi
    }
)



if client.schema.exists("Fund"):
    client.schema.delete_class("Fund")

if client.schema.exists("Question"):
    client.schema.delete_class("Question")


if not client.schema.exists("ArticleSaved"):
    client.schema.create_class(class_saved_article)

if not client.schema.exists("SavedNews"):
    client.schema.create_class(class_saved_news)

if not client.schema.exists("OrganizationSaved"):
    client.schema.create_class(class_saved_organization)



# if not client.schema.exists("ArticleSaved"):
#     client.schema.create_class(class_saved_article)

