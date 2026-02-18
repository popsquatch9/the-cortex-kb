"""
Semantic Search and Reasoning Module
Provides intelligent search and understanding capabilities
"""

from typing import List, Dict, Any, Optional
import numpy as np
from sentence_transformers import SentenceTransformer


class SemanticEngine:
    """Handles semantic understanding and reasoning"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the semantic engine
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        self.model_name = model_name
        self.model = None
        self.embeddings_cache: Dict[str, np.ndarray] = {}
    
    def _init_model(self):
        """Lazily initialize the model on first use"""
        if self.model is None:
            try:
                self.model = SentenceTransformer(self.model_name)
            except Exception as e:
                print(f"Warning: Could not load sentence transformer model: {e}")
                print("Falling back to simple text similarity.")
                self.model = "fallback"
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for text
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        if text in self.embeddings_cache:
            return self.embeddings_cache[text]
        
        self._init_model()
        
        if self.model == "fallback":
            # Simple fallback: use character frequency as a simple embedding
            embedding = self._simple_embedding(text)
        else:
            embedding = self.model.encode(text, convert_to_numpy=True)
        
        self.embeddings_cache[text] = embedding
        return embedding
    
    def _simple_embedding(self, text: str) -> np.ndarray:
        """Simple embedding for fallback mode"""
        # Create a simple 384-dimensional embedding based on text features
        text_lower = text.lower()
        features = np.zeros(384)
        
        # Use simple text statistics
        words = text_lower.split()
        if words:
            features[0] = len(words)
            features[1] = len(text)
            features[2] = sum(len(w) for w in words) / len(words)  # avg word length
            
            # Use hash of words to populate the rest
            for i, word in enumerate(words[:100]):
                idx = hash(word) % 381 + 3
                features[idx] += 1
        
        # Normalize
        norm = np.linalg.norm(features)
        if norm > 0:
            features = features / norm
        
        return features
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """
        Compute semantic similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0.0 - 1.0)
        """
        emb1 = self.embed_text(text1)
        emb2 = self.embed_text(text2)
        
        # Cosine similarity
        similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        
        # Convert to 0-1 range
        return float((similarity + 1) / 2)
    
    def find_similar_documents(
        self, 
        query: str, 
        documents: List[Dict[str, Any]], 
        top_k: int = 5,
        threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Find documents semantically similar to a query
        
        Args:
            query: Search query
            documents: List of document dictionaries
            top_k: Number of top results to return
            threshold: Minimum similarity threshold
            
        Returns:
            List of similar documents with similarity scores
        """
        query_embedding = self.embed_text(query)
        
        results = []
        for doc in documents:
            content = str(doc.get('content', ''))
            if not content:
                continue
            
            doc_embedding = self.embed_text(content)
            similarity = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )
            similarity = float((similarity + 1) / 2)
            
            if similarity >= threshold:
                results.append({
                    **doc,
                    'similarity': similarity
                })
        
        # Sort by similarity and return top_k
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]
    
    def extract_key_concepts(self, text: str) -> List[str]:
        """
        Extract key concepts from text (simplified version)
        
        Args:
            text: Text to analyze
            
        Returns:
            List of key concepts
        """
        # Simple implementation: extract longer words and phrases
        words = text.split()
        concepts = []
        
        for word in words:
            # Remove punctuation
            clean_word = ''.join(c for c in word if c.isalnum())
            # Keep words longer than 4 characters
            if len(clean_word) > 4:
                concepts.append(clean_word.lower())
        
        # Return unique concepts
        return list(set(concepts))[:10]
    
    def categorize_content(self, text: str) -> str:
        """
        Automatically categorize content (simplified version)
        
        Args:
            text: Text to categorize
            
        Returns:
            Category name
        """
        text_lower = text.lower()
        
        # Simple keyword-based categorization
        if any(word in text_lower for word in ['code', 'programming', 'function', 'class', 'import']):
            return 'programming'
        elif any(word in text_lower for word in ['research', 'study', 'paper', 'article']):
            return 'research'
        elif any(word in text_lower for word in ['note', 'memo', 'reminder', 'todo']):
            return 'notes'
        elif any(word in text_lower for word in ['data', 'analysis', 'statistics', 'dataset']):
            return 'data'
        else:
            return 'general'
