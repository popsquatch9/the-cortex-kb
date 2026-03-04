"""
Semantic Search and Reasoning Module
Provides intelligent search and understanding capabilities
"""

import os
from typing import List, Dict, Any, Optional
import numpy as np

# Lazy import – sentence_transformers pulls in torch which may not work on
# every Python version (e.g. 3.14).  We defer the import to first use so
# the rest of the application can still start up with fallback similarity.
SentenceTransformer = None  # will be set by _lazy_import_st()

def _lazy_import_st():
    global SentenceTransformer
    if SentenceTransformer is not None:
        return
    try:
        from sentence_transformers import SentenceTransformer as _ST
        SentenceTransformer = _ST
    except Exception as e:
        print(f"Warning: Could not import sentence_transformers: {e}")
        print("Falling back to simple text similarity.")

try:
    from .llm_provider import LLMClient
except ImportError:
    LLMClient = None


class SemanticEngine:
    """Handles semantic understanding and reasoning"""
    
    # Embedding dimensions for fallback mode
    EMBEDDING_DIM = 384
    # Index offset for word hashing in fallback embeddings
    HASH_OFFSET = 3
    # Max words to use for hashing in fallback embeddings  
    MAX_HASH_WORDS = 100
    
    def __init__(
        self, 
        model_name: str = "all-MiniLM-L6-v2",
        llm_provider: Optional[str] = None,
        llm_api_key: Optional[str] = None
    ):
        """
        Initialize the semantic engine
        
        Args:
            model_name: Name of the sentence transformer model to use
            llm_provider: LLM provider to use ('claude', 'gemini', or None)
            llm_api_key: API key for LLM provider (optional, uses env var)
        """
        self.model_name = model_name
        self.model = None
        self.embeddings_cache: Dict[str, np.ndarray] = {}
        
        # Initialize LLM client if requested
        self.llm_client = None
        if llm_provider and LLMClient:
            try:
                self.llm_client = LLMClient(provider=llm_provider, api_key=llm_api_key)
            except Exception as e:
                print(f"Warning: Could not initialize LLM provider: {e}")
                print("Continuing with local models only.")
    
    def _init_model(self):
        """Lazily initialize the model on first use"""
        if self.model is None:
            _lazy_import_st()
            try:
                if SentenceTransformer is not None:
                    self.model = SentenceTransformer(self.model_name)
                else:
                    raise RuntimeError("sentence_transformers unavailable")
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
        # Create a simple embedding based on text features
        text_lower = text.lower()
        features = np.zeros(self.EMBEDDING_DIM)
        
        # Use simple text statistics
        words = text_lower.split()
        if words:
            features[0] = len(words)
            features[1] = len(text)
            features[2] = sum(len(w) for w in words) / len(words)  # avg word length
            
            # Use hash of words to populate the rest
            for i, word in enumerate(words[:self.MAX_HASH_WORDS]):
                idx = hash(word) % (self.EMBEDDING_DIM - self.HASH_OFFSET) + self.HASH_OFFSET
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
        
        return self._cosine_similarity(emb1, emb2)
    
    def _cosine_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings
        
        Args:
            emb1: First embedding
            emb2: Second embedding
            
        Returns:
            Similarity score (0.0 - 1.0)
        """
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)
        
        # Handle zero norms
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # Cosine similarity
        similarity = np.dot(emb1, emb2) / (norm1 * norm2)
        
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
            similarity = self._cosine_similarity(query_embedding, doc_embedding)
            
            if similarity >= threshold:
                results.append({
                    **doc,
                    'similarity': similarity
                })
        
        # Sort by similarity and return top_k
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]
    
    def extract_key_concepts(self, text: str, use_llm: bool = True) -> List[str]:
        """
        Extract key concepts from text
        
        Args:
            text: Text to analyze
            use_llm: Whether to use LLM for extraction if available
            
        Returns:
            List of key concepts
        """
        # Use LLM if available and requested
        if use_llm and self.llm_client and self.llm_client.is_available():
            try:
                return self.llm_client.extract_key_concepts(text)
            except Exception as e:
                print(f"Warning: LLM concept extraction failed: {e}")
                print("Falling back to simple extraction.")
        
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
    
    def categorize_content(self, text: str, use_llm: bool = True) -> str:
        """
        Automatically categorize content
        
        Args:
            text: Text to categorize
            use_llm: Whether to use LLM for categorization if available
            
        Returns:
            Category name
        """
        # Use LLM if available and requested
        if use_llm and self.llm_client and self.llm_client.is_available():
            try:
                return self.llm_client.categorize(text)
            except Exception as e:
                print(f"Warning: LLM categorization failed: {e}")
                print("Falling back to simple categorization.")
        
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
    
    def summarize(self, text: str, max_length: int = 200) -> str:
        """
        Summarize text
        
        Args:
            text: Text to summarize
            max_length: Maximum length in words
            
        Returns:
            Summary text
        """
        if self.llm_client and self.llm_client.is_available():
            try:
                return self.llm_client.summarize(text, max_length)
            except Exception as e:
                print(f"Warning: LLM summarization failed: {e}")
                print("Falling back to simple truncation.")
        
        # Fallback: simple truncation
        words = text.split()
        if len(words) <= max_length:
            return text
        return ' '.join(words[:max_length]) + '...'
    
    def answer_question(self, question: str, context: str) -> str:
        """
        Answer a question based on context
        
        Args:
            question: Question to answer
            context: Context to use for answering
            
        Returns:
            Answer text
        """
        if self.llm_client and self.llm_client.is_available():
            try:
                return self.llm_client.answer_question(question, context)
            except Exception as e:
                print(f"Warning: LLM question answering failed: {e}")
                return "LLM not available or error occurred."
        
        return "LLM not available. Please configure Claude or Gemini API."
    
    def generate_insights(self, text: str) -> str:
        """
        Generate insights about text
        
        Args:
            text: Text to analyze
            
        Returns:
            Insights text
        """
        if self.llm_client and self.llm_client.is_available():
            try:
                return self.llm_client.generate_insights(text)
            except Exception as e:
                print(f"Warning: LLM insight generation failed: {e}")
                return "LLM not available or error occurred."
        
        return "LLM not available. Please configure Claude or Gemini API."
