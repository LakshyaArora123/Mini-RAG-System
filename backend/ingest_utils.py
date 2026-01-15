from pathlib import Path
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid
from pypdf import PdfReader
from dotenv import load_dotenv
import os

load_dotenv(Path(__file__).parent / ".env")

COLLECTION = "mini_rag_local"

model = SentenceTransformer("all-MiniLM-L6-v2")

from backend.qdrant_client import client, COLLECTION


def extract_text(file_path: Path) -> str:
    if file_path.suffix.lower() == ".pdf":
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    return file_path.read_text(encoding="utf-8", errors="ignore")


def ingest_file(file_path: Path):
    text = extract_text(file_path)

    chunks = []
    size = 500
    for i in range(0, len(text), size):
        chunks.append(text[i:i + size])

    vectors = model.encode(chunks).tolist()

    points = []
    for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text": chunk,
                    "source": file_path.name,
                    "chunk_id": i
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION,
        points=points
    )

    return len(points)
