import os, re
from google import genai
from dotenv import load_dotenv
from qdrant_client.models import Filter, FieldCondition, MatchValue
from qdrant_client import QdrantClient

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv('backend/.env', override=True)

client_gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

COLLECTION = "mini_rag_loc"

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
    timeout=30
)


def gemini_embed(text: str) -> list[float]:
    response = client_gemini.models.embed_content(
        model="text-embedding-004",
        contents=[text]
    )
    return response.embeddings[0].values

def fetch_all_chunks(source: str, limit: int = 100):
    results = client.scroll(
        collection_name=COLLECTION,
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="source",
                    match=MatchValue(value=source)
                )
            ]
        ),
        limit=limit
    )[0]

    return [r.payload["text"] for r in results]

def summarize_document(source: str):
    chunks = fetch_all_chunks(source)

    if not chunks:
        return {
            "source": source,
            "summary": "No content found for this document."
        }

    context = "\n\n".join(chunks[:20])

    prompt = f"""
You are an expert assistant.

Summarize the following document clearly and concisely.
Use your own words.
Do not quote verbatim.
Focus on key ideas, concepts, and structure.

Document content:
{context}

Summary:
"""
    response = client_gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return {
        "source": source,
        "summary": response.text.strip()
    }

def gemini_synthesize_answer(query: str, contexts: list[str]) -> str:
    if not contexts:
        return "I do not know based on the provided context."

    context_block = "\n\n".join(contexts)

    prompt = f"""
You are a knowledgeable assistant.

Use ONLY the information from the context below.
Do NOT copy sentences verbatim.
Explain in your own words.
If the answer is not present, say you don't know.

Context:
{context_block}

Question:
{query}

Answer:
""".strip()

    response = client_gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()

RELEVANCE_THRESHOLD = 0.3
def answer_query(query, top_k=5, source=None):
    SUMMARY_TRIGGERS = ["summarize", "summary", "overview", "give an overview"]

    if any(t in query.lower() for t in SUMMARY_TRIGGERS) and source:
        return summarize_document(source)

    query_vec = gemini_embed(query)

    if source:
        results = client.query_points(
            collection_name=COLLECTION,
            query=query_vec,
            limit=top_k,
            with_payload=True,
            filter=Filter(
                must=[
                    FieldCondition(
                        key="source",
                        match=MatchValue(value=source)
                    )
                ]
            )
        )
    else:
        results = client.query_points(
            collection_name=COLLECTION,
            query=query_vec,
            limit=top_k,
            with_payload=True
        )

    if not results or not results.points:
        return {
            "query": query,
            "final_answer": "I do not know based on the provided context.",
            "top_contexts": []
        }

    top_contexts = [p.payload for p in results.points[:3]]
    context_texts = [c["text"] for c in top_contexts]

    try:
        final_answer = gemini_synthesize_answer(query, context_texts)
    except Exception:
        final_answer = top_contexts[0]["text"]

    return {
        "query": query,
        "final_answer": final_answer,
        "top_contexts": top_contexts
    }
