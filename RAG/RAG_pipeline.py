import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict
import json

class TelcoRAGPipeline:
    def __init__(self, knowledge_base: List[Dict], model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.knowledge_base = knowledge_base
        self.documents = [doc["content"] for doc in knowledge_base]
        self.metadata = [{"title": doc["title"], "category": doc["category"]} for doc in knowledge_base]
        
        # Create vector index
        self.index = self._build_index()
    
    def _build_index(self):
        """Build FAISS index from documents"""
        embeddings = self.model.encode(self.documents)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        index.add(embeddings.astype('float32'))
        
        return index
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve relevant documents for query"""
        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx != -1:  # Valid result
                results.append({
                    "content": self.documents[idx],
                    "metadata": self.metadata[idx],
                    "score": float(score),
                    "rank": i + 1
                })
        
        return results
    
    def get_context(self, query: str, top_k: int = 3) -> str:
        """Get formatted context for LLM"""
        retrieved_docs = self.retrieve(query, top_k)
        
        if not retrieved_docs:
            return "No relevant information found in knowledge base."
        
        context_parts = []
        for doc in retrieved_docs:
            context_parts.append(f"Source: {doc['metadata']['title']}\n{doc['content']}")
        
        return "\n\n".join(context_parts)
