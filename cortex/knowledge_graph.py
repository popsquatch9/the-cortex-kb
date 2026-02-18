"""
Knowledge Graph Module
Manages the knowledge base structure and relationships
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class KnowledgeGraph:
    """Manages knowledge as a graph structure with nodes and relationships"""
    
    def __init__(self, storage_path: str = "./cortex_data"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.nodes_file = self.storage_path / "nodes.json"
        self.edges_file = self.storage_path / "edges.json"
        
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, Any]] = []
        
        self._load()
    
    def _load(self):
        """Load graph from disk"""
        if self.nodes_file.exists():
            with open(self.nodes_file, 'r') as f:
                self.nodes = json.load(f)
        
        if self.edges_file.exists():
            with open(self.edges_file, 'r') as f:
                self.edges = json.load(f)
    
    def _save(self):
        """Save graph to disk"""
        with open(self.nodes_file, 'w') as f:
            json.dump(self.nodes, f, indent=2)
        
        with open(self.edges_file, 'w') as f:
            json.dump(self.edges, f, indent=2)
    
    def add_node(self, node_id: str, data: Dict[str, Any]) -> str:
        """
        Add a node to the knowledge graph
        
        Args:
            node_id: Unique identifier for the node
            data: Node data including content and metadata
            
        Returns:
            The node ID
        """
        self.nodes[node_id] = {
            **data,
            'id': node_id,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        self._save()
        return node_id
    
    def update_node(self, node_id: str, data: Dict[str, Any]) -> bool:
        """
        Update an existing node with new data
        
        Args:
            node_id: Node ID to update
            data: Data to update in the node
            
        Returns:
            True if successful, False if node doesn't exist
        """
        if node_id not in self.nodes:
            return False
        
        self.nodes[node_id].update(data)
        self.nodes[node_id]['updated_at'] = datetime.now().isoformat()
        self._save()
        return True
    
    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Get a node by ID"""
        return self.nodes.get(node_id)
    
    def add_edge(self, source_id: str, target_id: str, relationship: str, weight: float = 1.0):
        """
        Add an edge between two nodes
        
        Args:
            source_id: Source node ID
            target_id: Target node ID
            relationship: Type of relationship
            weight: Strength of relationship (0.0 - 1.0)
        """
        edge = {
            'source': source_id,
            'target': target_id,
            'relationship': relationship,
            'weight': weight,
            'created_at': datetime.now().isoformat()
        }
        self.edges.append(edge)
        self._save()
    
    def get_related_nodes(self, node_id: str, relationship: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all nodes related to a given node
        
        Args:
            node_id: The node to find relationships for
            relationship: Optional filter by relationship type
            
        Returns:
            List of related nodes
        """
        related = []
        for edge in self.edges:
            if edge['source'] == node_id:
                if relationship is None or edge['relationship'] == relationship:
                    target = self.get_node(edge['target'])
                    if target:
                        related.append(target)
            elif edge['target'] == node_id:
                if relationship is None or edge['relationship'] == relationship:
                    source = self.get_node(edge['source'])
                    if source:
                        related.append(source)
        
        return related
    
    def search_nodes(self, query: str) -> List[Dict[str, Any]]:
        """
        Simple text search across nodes
        
        Args:
            query: Search query
            
        Returns:
            List of matching nodes
        """
        results = []
        query_lower = query.lower()
        
        for node_id, node in self.nodes.items():
            content = str(node.get('content', '')).lower()
            name = str(node.get('name', '')).lower()
            
            if query_lower in content or query_lower in name:
                results.append(node)
        
        return results
    
    def get_all_nodes(self) -> List[Dict[str, Any]]:
        """Get all nodes in the graph"""
        return list(self.nodes.values())
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the knowledge graph"""
        return {
            'total_nodes': len(self.nodes),
            'total_edges': len(self.edges),
            'node_types': self._count_node_types(),
            'relationship_types': self._count_relationship_types()
        }
    
    def _count_node_types(self) -> Dict[str, int]:
        """Count nodes by type"""
        types = {}
        for node in self.nodes.values():
            node_type = node.get('type', 'unknown')
            types[node_type] = types.get(node_type, 0) + 1
        return types
    
    def _count_relationship_types(self) -> Dict[str, int]:
        """Count edges by relationship type"""
        types = {}
        for edge in self.edges:
            rel_type = edge.get('relationship', 'unknown')
            types[rel_type] = types.get(rel_type, 0) + 1
        return types
