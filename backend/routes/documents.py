from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from pathlib import Path
from backend.utils.document_parser import load_documents, chunk_text
from backend.utils.vector_store import vector_store

router = APIRouter(prefix="/api/documents", tags=["documents"])
DATA_DIR = Path("backend/data/sample-docs")
DATA_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(('.txt', '.md')):
        raise HTTPException(status_code=400, detail="Only .txt and .md files are allowed.")
    
    file_path = DATA_DIR / file.filename
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        return {"message": f"Successfully uploaded {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reindex")
async def reindex_documents():
    try:
        docs = load_documents(str(DATA_DIR))
        total_chunks = 0
        for doc in docs:
            chunks = chunk_text(doc["content"])
            vector_store.add_chunks(chunks, doc["filename"])
            total_chunks += len(chunks)
        return {"message": "Successfully reindexed documents.", "chunks_processed": total_chunks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
