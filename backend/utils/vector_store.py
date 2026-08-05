import os
import faiss
import numpy as np
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Dimensionality of text-embedding-3-small
EMBEDDING_DIM = 1536 

class VectorStore:
    def __init__(self):
        self.index = faiss.IndexFlatL2(EMBEDDING_DIM)
        self.metadata: List[Dict[str, Any]] = []
        
    def get_embedding(self, text: str) -> List[float]:
        """Fetch embedding from OpenAI."""
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
        
    def add_chunks(self, chunks: List[str], source_filename: str):
        """Embed and add chunks to the FAISS index."""
        if not chunks:
            return
            
        embeddings = []
        for i, chunk in enumerate(chunks):
            emb = self.get_embedding(chunk)
            embeddings.append(emb)
            self.metadata.append({
                "filename": source_filename,
                "chunk_index": i,
                "text": chunk
            })
            
        # Add to FAISS index
        embeddings_np = np.array(embeddings).astype('float32')
        self.index.add(embeddings_np)
        
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search for top_k most similar chunks."""
        if self.index.ntotal == 0:
            return []
            
        query_emb = self.get_embedding(query)
        query_np = np.array([query_emb]).astype('float32')
        
        distances, indices = self.index.search(query_np, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                results.append({
                    "distance": float(distances[0][i]),
                    "metadata": self.metadata[idx]
                })
        return results

# Singleton instance for the app
vector_store = VectorStore()
