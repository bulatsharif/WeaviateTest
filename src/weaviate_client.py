from dotenv import load_dotenv
import weaviate
import os

from src.schemas import class_article, class_requests, class_saved_news, class_news, class_saved_organization, \
    class_organization, class_saved_article

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

if not client.schema.exists("Article"):
    client.schema.create_class(class_article)

if not client.schema.exists("ArticleSaved"):
    client.schema.create_class(class_saved_article)

if not client.schema.exists("Organization"):
    client.schema.create_class(class_organization)

if not client.schema.exists("OrganizationSaved"):
    client.schema.create_class(class_saved_organization)

if not client.schema.exists("News"):
    client.schema.create_class(class_news)

if not client.schema.exists("SavedNews"):
    client.schema.create_class(class_saved_news)

if not client.schema.exists("Request"):
    client.schema.create_class(class_requests)











