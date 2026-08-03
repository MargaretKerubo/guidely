# 📚 Guidely - Internal Knowledge Assistant

Guidely is an internal support assistant designed to help team members quickly find accurate, plain-language answers from company documents without digging through pages of text[cite: 1, 4]. Powered by **Retrieval-Augmented Generation (RAG)**, Guidely combines semantic search with real-time text generation while always providing clear citations for its sources[cite: 2, 5].

---

## 🛠️ Tech Stack

* [cite_start]**Frontend:** React (Vite), Tailwind CSS, Lucide Icons [cite: 2, 45]
* [cite_start]**Backend:** FastAPI (Python), Uvicorn [cite: 2, 43]
* [cite_start]**Embeddings & LLM:** OpenAI API (`text-embedding-3-small`, `gpt-4o-mini` / `gpt-3.5-turbo`) [cite: 9, 50, 55]
* [cite_start]**Vector Store:** FAISS [cite: 9, 51]
* [cite_start]**Environment Management:** `python-dotenv` [cite: 18, 43]

---

## 🏗️ Pipeline Architecture

1. [cite_start]**Document Ingestion & Chunking:** Ingests plain text and markdown documents from `/data/sample-docs/` [cite: 8, 16, 47][cite_start], splitting them into small context chunks (~500–1,000 tokens) with overlap[cite: 9, 48].
2. [cite_start]**Hashing & Caching:** Computes SHA256 hashes of files to prevent re-embedding unchanged documents[cite: 26, 27, 51, 52].
3. [cite_start]**Vector Embeddings & Indexing:** Converts text chunks into vector embeddings via OpenAI and stores them in a local FAISS index[cite: 9, 50, 51].
4. [cite_start]**Retrieval & RAG Generation:** * Embeds the user query[cite: 10].
   * [cite_start]Retrieves top-$k$ ($k=3$) most similar text snippets[cite: 10, 22, 53].
   * [cite_start]Sends snippets and the user query to the LLM with instructions to cite sources[cite: 11, 54, 55].
5. [cite_start]**Response:** Returns clean JSON containing the answer along with referenced filenames and snippets[cite: 11, 16, 55].

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
[cite_start]
http://googleusercontent.com/immersive_entry_chip/0

Frontend will be running at: `http://localhost:5173`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/search` | [cite_start]Submits user prompt; performs vector search & generates RAG answer with sources[cite: 15, 58]. |
| `POST` | `/api/documents/upload` | [cite_start]Uploads raw documents (`.txt`, `.md`) to data directory[cite: 13, 56]. |
| `POST` | `/api/documents/reindex` | [cite_start]Triggers document ingestion, chunking, and FAISS indexing[cite: 13, 57]. |
| `GET` | `/health` | [cite_start]API health status[cite: 34]. |

---

## 📊 Testing & Benchmark Metrics

[cite_start]The system performance and quality targets are tracked below:

| Metric | Category | Target | Current Benchmark | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Retrieval@3** | Manual | [cite_start]$\ge 80\%$ top-3 accuracy [cite: 22] | *TBD* | ⏳ Pending |
| **Answer Reference Coverage** | Manual | [cite_start]$\ge 90\%$ answers with citations [cite: 24] | *TBD* | ⏳ Pending |
| **Source Precision** | Manual | [cite_start]$\ge 80\%$ snippet relevance [cite: 30] | *TBD* | ⏳ Pending |
| **Latency (Median)** | Auto-logged | [cite_start]$< 3\text{s}$ (cached) [cite: 25] | *TBD* | ⏳ Pending |
| **Latency (p95)** | Auto-logged | [cite_start]$< 5\text{s}$ [cite: 25] | *TBD* | ⏳ Pending |
| **Embedding Cache Effectiveness** | Auto-logged | [cite_start]$100\%$ hits on unchanged docs [cite: 27] | *TBD* | ⏳ Pending |
| **Failure Handling** | Auto-logged | [cite_start]Graceful 4xx/5xx handling [cite: 29] | *TBD* | ⏳ Pending |

---

## 🛡️ Failure Handling

[cite_start]The API natively validates and gracefully handles common failure modes[cite: 16, 28]:
* [cite_start]**Empty Query:** Returns HTTP `400 Bad Request`[cite: 28, 29, 60].
* [cite_start]**Missing API Key:** Logs backend configuration failure and returns HTTP `500 Server Error`[cite: 28, 29, 60].
* [cite_start]**Corrupted/Unreadable File:** Skips corrupted files during ingestion and logs error[cite: 28, 29, 60].
* [cite_start]**No Relevant Documents Found:** Returns fallback response indicating lack of context rather than hallucinating[cite: 28, 29, 60].