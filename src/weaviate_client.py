from dotenv import load_dotenv
import weaviate
import os

from src.schemas import class_organization, class_news

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

if client.schema.exists('Organization'):
    client.schema.delete_class('Organization')
    client.schema.create_class(class_organization)

if client.schema.exists('News'):
    client.schema.delete_class('News')
    client.schema.create_class(class_news)
