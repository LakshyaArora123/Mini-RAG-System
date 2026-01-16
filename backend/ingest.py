import os
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

load_dotenv('backend/.env', override=True)

from google import genai
client_gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
def gemini_embed(text: str) -> list[float]:
    response = client_gemini.models.embed_content(
        model="text-embedding-004",
        content=text
    )
    return response.embedding

COLLECTION = "mini_rag_loc"

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
    timeout=30
)

if not client.collection_exists(COLLECTION):
    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(
            size=768,
            distance=Distance.COSINE
        )
    )

texts = [
    "Retrieval-Augmented Generation (RAG) combines information retrieval with language models to generate grounded responses.",
    "In RAG systems, documents are stored in a vector database and retrieved at query time."
]

points = []
for i, text in enumerate(texts):
    vec = gemini_embed(text)
    points.append(
        PointStruct(
            id=i,
            vector=vec,
            payload={
                "text": text,
                "source": "manual_seed",
                "chunk_id": i
            }
        )
    )

client.upsert(
    collection_name=COLLECTION,
    points=points
)

print("✅ Ingestion complete — payloads written safely")
