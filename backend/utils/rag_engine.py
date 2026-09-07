import os
import json
from typing import Dict, Any, List
from groq import Groq
from backend.utils.vector_store import vector_store

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(query: str) -> Dict[str, Any]:
    """
    Search vector store for relevant chunks and generate an answer using LLM.
    """
    # Retrieve top 3 relevant chunks
    search_results = vector_store.search(query, top_k=3)
    
    if not search_results:
        return {
            "answer": "I'm sorry, but I couldn't find any relevant information in the knowledge base to answer your question.",
            "sources": []
        }

    # Prepare context
    context_text = ""
    sources = []
    
    for idx, result in enumerate(search_results):
        meta = result["metadata"]
        snippet = meta["text"]
        filename = meta["filename"]
        
        context_text += f"\n--- Document: {filename} (Snippet {idx+1}) ---\n{snippet}\n"
        
        sources.append({
            "filename": filename,
            "snippet": snippet[:200] + "..." if len(snippet) > 200 else snippet
        })
        
    # Construct prompt
    system_prompt = (
        "You are an internal knowledge assistant for a company. "
        "Use the provided document snippets to answer the user's question accurately. "
        "Always synthesize a clear, plain-language answer. "
        "Do not use outside information; if the answer is not in the context, state that clearly."
    )
    
    user_prompt = f"Context:\n{context_text}\n\nQuestion: {query}"
    
    # Call LLM
    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )
    
    answer = response.choices[0].message.content
    
    return {
        "answer": answer,
        "sources": sources
    }
