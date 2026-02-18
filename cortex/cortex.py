"""
Main Cortex Knowledge Base Class
Orchestrates all components of the knowledge base system
"""

import os
import hashlib
from typing import List, Dict, Any, Optional
from pathlib import Path

from .ingestion import DocumentIngester
from .knowledge_graph import KnowledgeGraph
from .semantic_engine import SemanticEngine
from .source_discovery import SourceDiscovery


class CortexKB:
    """
    Smart Personal Knowledge Base
    
    A system that reads, reasons, understands, and organizes information,
    and discovers related external sources to build a comprehensive knowledge base.
    """
    
    def __init__(
        self, 
        storage_path: str = "./cortex_data",
        enable_external_sources: bool = True,
        relevance_threshold: float = 0.7
    ):
        """
        Initialize the Cortex Knowledge Base
        
        Args:
            storage_path: Directory for storing knowledge base data
            enable_external_sources: Whether to fetch external sources
            relevance_threshold: Minimum relevance score for content (0.0 - 1.0)
        """
        self.storage_path = Path(storage_path)
        self.enable_external_sources = enable_external_sources
        self.relevance_threshold = relevance_threshold
        
        # Initialize components
        self.ingester = DocumentIngester()
        self.graph = KnowledgeGraph(storage_path)
        self.semantic_engine = SemanticEngine()
        self.source_discovery = SourceDiscovery()
    
    def add_document(self, file_path: str, discover_sources: bool = True) -> str:
        """
        Add a document to the knowledge base
        
        Args:
            file_path: Path to the document
            discover_sources: Whether to discover related external sources
            
        Returns:
            Document ID
        """
        # Ingest the document
        doc = self.ingester.read_file(file_path)
        
        # Generate a unique ID
        doc_id = self._generate_id(doc['path'])
        
        # Add to knowledge graph
        self.graph.add_node(doc_id, doc)
        
        # Extract key concepts and categorize
        content = str(doc.get('content', ''))
        concepts = self.semantic_engine.extract_key_concepts(content)
        category = self.semantic_engine.categorize_content(content)
        
        # Update node with additional metadata
        self.graph.update_node(doc_id, {
            'concepts': concepts,
            'category': category
        })
        
        # Find related existing documents
        self._link_related_documents(doc_id, content)
        
        # Discover and add external sources if enabled
        if discover_sources and self.enable_external_sources:
            self._discover_and_add_sources(doc_id, content)
        
        return doc_id
    
    def add_text(
        self, 
        text: str, 
        metadata: Optional[Dict[str, Any]] = None,
        discover_sources: bool = True
    ) -> str:
        """
        Add raw text to the knowledge base
        
        Args:
            text: Text content
            metadata: Optional metadata
            discover_sources: Whether to discover related external sources
            
        Returns:
            Document ID
        """
        # Ingest the text
        doc = self.ingester.read_text(text, metadata)
        
        # Generate a unique ID
        doc_id = self._generate_id(text)
        
        # Add to knowledge graph
        self.graph.add_node(doc_id, doc)
        
        # Extract key concepts and categorize
        concepts = self.semantic_engine.extract_key_concepts(text)
        category = self.semantic_engine.categorize_content(text)
        
        # Update node with additional metadata
        self.graph.update_node(doc_id, {
            'concepts': concepts,
            'category': category
        })
        
        # Find related existing documents
        self._link_related_documents(doc_id, text)
        
        # Discover and add external sources if enabled
        if discover_sources and self.enable_external_sources:
            self._discover_and_add_sources(doc_id, text)
        
        return doc_id
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search the knowledge base
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        all_docs = self.graph.get_all_nodes()
        
        # Use semantic search
        results = self.semantic_engine.find_similar_documents(
            query, 
            all_docs, 
            top_k=top_k,
            threshold=self.relevance_threshold
        )
        
        return results
    
    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a document by ID
        
        Args:
            doc_id: Document ID
            
        Returns:
            Document data or None if not found
        """
        return self.graph.get_node(doc_id)
    
    def get_related_documents(self, doc_id: str) -> List[Dict[str, Any]]:
        """
        Get documents related to a given document
        
        Args:
            doc_id: Document ID
            
        Returns:
            List of related documents
        """
        return self.graph.get_related_nodes(doc_id)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get knowledge base statistics
        
        Returns:
            Statistics dictionary
        """
        return self.graph.get_statistics()
    
    def organize_by_category(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Organize all documents by category
        
        Returns:
            Dictionary mapping categories to documents
        """
        all_docs = self.graph.get_all_nodes()
        categories: Dict[str, List[Dict[str, Any]]] = {}
        
        for doc in all_docs:
            category = doc.get('category', 'general')
            if category not in categories:
                categories[category] = []
            categories[category].append(doc)
        
        return categories
    
    def _generate_id(self, content: str) -> str:
        """Generate a unique ID for content"""
        return hashlib.md5(content.encode()).hexdigest()
    
    def _link_related_documents(self, doc_id: str, content: str):
        """Find and link related documents based on semantic similarity"""
        all_docs = self.graph.get_all_nodes()
        
        for other_doc in all_docs:
            if other_doc['id'] == doc_id:
                continue
            
            other_content = str(other_doc.get('content', ''))
            similarity = self.semantic_engine.compute_similarity(content, other_content)
            
            if similarity >= self.relevance_threshold:
                self.graph.add_edge(
                    doc_id, 
                    other_doc['id'], 
                    'related_to',
                    weight=similarity
                )
    
    def _discover_and_add_sources(self, parent_doc_id: str, content: str):
        """Discover and add external sources related to content"""
        # Get existing URLs to avoid duplicates
        existing_urls = [
            node.get('url') 
            for node in self.graph.get_all_nodes() 
            if node.get('url')
        ]
        
        # Discover sources
        sources = self.source_discovery.discover_related_sources(content, existing_urls)
        
        # Add each source to the knowledge base
        for source in sources:
            # Vet the source
            vetted_source = self.source_discovery.vet_source(source)
            
            # Only add if quality score is acceptable
            if vetted_source.get('quality_score', 0) >= 0.5:
                source_id = self._generate_id(vetted_source['url'])
                self.graph.add_node(source_id, vetted_source)
                
                # Link to parent document
                self.graph.add_edge(
                    parent_doc_id,
                    source_id,
                    'has_source',
                    weight=vetted_source.get('quality_score', 0.5)
                )
