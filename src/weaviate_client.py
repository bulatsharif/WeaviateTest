from dotenv import load_dotenv
import weaviate
import os

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