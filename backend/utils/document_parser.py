import os
import hashlib
from typing import List, Dict

def calculate_file_hash(filepath: str) -> str:
    """Calculate MD5 hash of a file to check if it has changed."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def load_documents(directory: str) -> List[Dict]:
    """Load text documents from a directory."""
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt") or filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                file_hash = calculate_file_hash(filepath)
                documents.append({
                    "filename": filename,
                    "content": content,
                    "hash": file_hash
                })
    return documents

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks based on characters (approx token sizing)."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
