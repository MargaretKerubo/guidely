# 📚 Guidely - Internal Knowledge Assistant

Guidely is an internal support assistant designed to help team members quickly find accurate, plain-language answers from company documents without digging through pages of text. Powered by **Retrieval-Augmented Generation (RAG)**, Guidely combines semantic search with real-time text generation while always providing clear citations for its sources.

---

## 🛠️ Tech Stack

* **Frontend:** React (Vite), Tailwind CSS, Lucide Icons
* **Backend:** FastAPI (Python), Uvicorn
* **Embeddings & LLM:** OpenAI API (`text-embedding-3-small`, `gpt-4o-mini` / `gpt-3.5-turbo`)
* **Vector Store:** FAISS
* **Environment Management:** `python-dotenv`

---

## 🏗️ Pipeline Architecture

1. **Document Ingestion & Chunking:** Ingests plain text and markdown documents from `/data/sample-docs/`, splitting them into small context chunks (~500–1,000 tokens) with overlap.
2. **Hashing & Caching:** Computes SHA256 hashes of files to prevent re-embedding unchanged documents.
3. **Vector Embeddings & Indexing:** Converts text chunks into vector embeddings via OpenAI and stores them in a local FAISS index.
4. **Retrieval & RAG Generation:** * Embeds the user query.
   * Retrieves top-$k$ ($k=3$) most similar text snippets.
   * Sends snippets and the user query to the LLM with instructions to cite sources.
5. **Response:** Returns clean JSON containing the answer along with referenced filenames and snippets.

---

## 📁 Repository Structure

```text
guidely/
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/
│       ├── pages/
│       └── App.jsx
├── backend/
│   ├── main.py
│   ├── routes/
│   │   ├── documents.py
│   │   └── search.py
│   ├── models/
│   │   └── record.py
│   └── data/
│       └── sample-docs/
│           ├── policy.txt
│           ├── faq.txt
│           └── guide.txt
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MargaretKerubo/guidely.git
   cd guidely
   ```
2. **Backend Setup:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env # Add your OPENAI_API_KEY
   uvicorn main:app --reload --port 8000
   ```
3. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

Frontend will be running at: `http://localhost:5173`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/search` | Submits user prompt; performs vector search & generates RAG answer with sources. |
| `POST` | `/api/documents/upload` | Uploads raw documents (`.txt`, `.md`) to data directory. |
| `POST` | `/api/documents/reindex` | Triggers document ingestion, chunking, and FAISS indexing. |
| `GET` | `/health` | API health status. |

---

## 📊 Testing & Benchmark Metrics

The system performance and quality targets are tracked below:

| Metric | Category | Target | Current Benchmark | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Retrieval@3** | Manual | $\ge 80\%$ top-3 accuracy | > 85% | ✅ Pass |
| **Answer Reference Coverage** | Manual | $\ge 90\%$ answers with citations | > 95% | ✅ Pass |
| **Source Precision** | Manual | $\ge 80\%$ snippet relevance | > 85% | ✅ Pass |
| **Latency (Median)** | Auto-logged | $< 3\text{s}$ (cached) | ~ 0.5s | ✅ Pass |
| **Latency (p95)** | Auto-logged | $< 5\text{s}$ | < 2s | ✅ Pass |
| **Embedding Cache Effectiveness** | Auto-logged | $100\%$ hits on unchanged docs | 100% | ✅ Pass |
| **Failure Handling** | Auto-logged | Graceful 4xx/5xx handling | Passes tests | ✅ Pass |

---

## 🛡️ Failure Handling

The API natively validates and gracefully handles common failure modes:
* **Empty Query:** Returns HTTP `400 Bad Request`.
* **Missing API Key:** Logs backend configuration failure and returns HTTP `500 Server Error`.
* **Corrupted/Unreadable File:** Skips corrupted files during ingestion and logs error.
* **No Relevant Documents Found:** Returns fallback response indicating lack of context rather than hallucinating.