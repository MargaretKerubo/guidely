import os
import faiss
import numpy as np
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# Initialize local embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Dimensionality of all-MiniLM-L6-v2
EMBEDDING_DIM = 384 

class VectorStore:
    def __init__(self):
        self.index = faiss.IndexFlatL2(EMBEDDING_DIM)
        self.metadata: List[Dict[str, Any]] = []
        
    def get_embedding(self, text: str) -> List[float]:
        """Fetch embedding from local SentenceTransformer model."""
        # encode returns a numpy array, convert to list of floats
        embedding = model.encode(text)
        return embedding.tolist()
        
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
