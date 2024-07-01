import weaviate
import os

os.environ["JINA_AI_API_KEY"] = "your_jina_api_key"
os.environ["MISTRAL_AI_API_KEY"] = "your_mistral_api_key"
os.environ["HOST"] = "your_host"

jinaApi: str = os.getenv("JINA_AI_API_KEY")
mistralApi: str = os.getenv("MISTRAL_AI_API_KEY")
host: str = os.getenv("HOST")


print("--------------------------------------------")
print(host)
print(jinaApi)
print(mistralApi)
print("--------------------------------------------")

client = weaviate.Client(
    url=host,
    additional_headers={
        "X-Jinaai-Api-Key": jinaApi,
        "X-Mistral-Api-Key": mistralApi
    }
)