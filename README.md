# 📚 Mini-RAG System (Gemini + Qdrant)

A **production-ready Retrieval-Augmented Generation (RAG) system** that allows users to upload documents, store semantic embeddings in a vector database, and ask grounded questions powered by Google Gemini.

This project demonstrates **end-to-end backend engineering**, vector search, cloud deployment, and frontend-backend integration.

---

## 🔗 Live Deployment

* **Frontend (Vercel):** [https://mini-rag-system.vercel.app/](https://mini-rag-system.vercel.app/)
* **Backend (Railway):** [https://mini-rag-system-production.up.railway.app/](https://mini-rag-system-production.up.railway.app/)
* **API Docs:** `/docs` (FastAPI Swagger UI)

---

## 📌 What This Project Demonstrates

*✅ RAG pipeline design
*✅ Document ingestion & chunking
*✅ Embeddings with **Gemini**
*✅ Vector search with **Qdrant Cloud**
*✅ LLM-grounded answers (no hallucination)
*✅ Separate frontend & backend deployments
*✅ Real-world production debugging & fixes

---

## 🧠 High-Level Architecture

![Image](https://cdn.prod.website-files.com/636e9a9a8d334e3450b08cc9/66ec7a2ce46888a5b8d4f50c_66ec79aece12f878f6eb35ab_Retrieval%2520Augmented%2520Generation.webp)

![Image](https://miro.medium.com/v2/resize%3Afit%3A1400/0%2AKOpmpTSoSrxgMQAV)

**Flow overview:**

1. User uploads a document
2. Backend chunks & embeds content
3. Embeddings stored in Qdrant
4. User asks a question
5. Relevant chunks retrieved
6. Gemini generates a grounded answer

---

## 🔁 Detailed RAG Pipeline

![Image](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2024/03/13/BDB-3880_1.png)

![Image](https://thedataquarry.com/_astro/embedding-pipeline.7jg2V3To_1v9wsd.webp)

![Image](https://cdn.prod.website-files.com/640248e1fd70b63c09bd3d09/652c62561b4433a6c8d2cc51_Customizable%20re-ranking.png)

### 1️⃣ Document Ingestion

* PDF / TXT files uploaded via frontend
* Backend extracts raw text
* Text split into fixed-size chunks
* Each chunk embedded using **Gemini Embeddings**
* Stored in Qdrant with metadata (`source`, `chunk_id`)

### 2️⃣ Query Flow

* User query embedded with the same embedding model
* Vector similarity search in Qdrant
* Top-K relevant chunks selected
* Gemini LLM generates answer **only from retrieved context**

---

## 🧱 Tech Stack

### Frontend

* HTML + CSS + Vanilla JS
* Deployed on **Vercel**
* Talks to backend via REST APIs

### Backend

* **FastAPI** (Python)
* Deployed on **Railway**
* Async-safe request handling

### Vector Database

* **Qdrant Cloud**
* Cosine similarity search
* Metadata-filtered retrieval

### Embeddings & LLM

* **Gemini Embeddings** (`text-embedding-004`, 768-D)
* **Gemini 2.5 Flash** for answers & summaries

---

## ⚙️ API Endpoints

| Method | Endpoint   | Description                  |
| ------ | ---------- | ---------------------------- |
| POST   | `/upload`  | Upload & ingest document     |
| POST   | `/chat`    | Ask questions over documents |
| POST   | `/summary` | Generate document summary    |
| DELETE | `/clear`   | Clear vector store           |
| GET    | `/docs`    | Swagger API documentation    |

---

## 🧩 Key Design Decisions

### 🔹 Gemini Embeddings instead of Sentence-Transformers

* Avoids heavy PyTorch installs
* Faster cloud builds
* Consistent embedding quality

### 🔹 Qdrant Cloud

* Production-grade vector DB
* Metadata filtering
* Scales independently of backend

### 🔹 Strict Grounding

* LLM instructed to **only answer from retrieved chunks**
* If answer not present → `"I don't know based on provided context"`

---

## 🛠️ Challenges Solved

* Torch build failures → switched to Gemini embeddings
* Vector dimension mismatch → separate collections (384 vs 768)
* Qdrant API version mismatch → corrected `query_points()` usage
* CORS & deployment issues → fixed Railway + Vercel integration
* Frontend JS loading errors → corrected routing & static serving

This mirrors **real production debugging**, not toy demos.

---

## 🧪 Running Locally

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
# Open index.html in browser
```

---

## 🔐 Environment Variables

### Backend (`.env`)

```env
GEMINI_API_KEY=your_key
QDRANT_URL=https://your-qdrant-cloud-url
QDRANT_API_KEY=your_key
```

---

## 🚀 Future Improvements

* Streaming responses (SSE / WebSockets)
* Multi-document comparison
* Hybrid keyword + vector search
* Auth & per-user document isolation
* Chunk citation highlighting in UI
