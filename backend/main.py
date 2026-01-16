from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
from backend.qdrant_schema import ensure_payload_indexes
from backend.rag import answer_query
from backend.rag import summarize_document
from pathlib import Path


env_path = Path(__file__).parent / ".env"
load_dotenv(env_path, override=True)



UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Mini RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class ChatRequest(BaseModel):
    query: str
    history: List[str] = []



@app.on_event("startup")
def startup_event():
    ensure_payload_indexes()

class SummaryRequest(BaseModel):
    source: str

@app.post("/summary")
def summary(req: SummaryRequest):
    print("Summarizing:", req.source)
    return summarize_document(req.source)

@app.get("/query")
def query(q: str):
    return answer_query(q)



class ChatRequest(BaseModel):
    query: str
    history: list[str] = []
    source: str | None = None

@app.post("/chat")
def chat(req: ChatRequest):
    return answer_query(req.query, source=req.source)


from fastapi import UploadFile, File
from backend.ingest_utils import ingest_file  

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    ingest_file(file_path)

    return {
        "status": "uploaded",
        "filename": file.filename
    }


    
from backend.qdrant_client import client, COLLECTION
from qdrant_client.models import VectorParams, Distance

@app.delete("/clear")
def clear_documents():
    if client.collection_exists(COLLECTION):
        client.delete_collection(COLLECTION)

    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(
            size=768,
            distance=Distance.COSINE
        )
    )

    return {"status": "cleared"}

