"""
Document Ingestion Module
Handles reading and parsing various document formats
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any
import markdown


class DocumentIngester:
    """Ingests and processes documents from various sources"""
    
    def __init__(self):
        self.supported_formats = ['.txt', '.md', '.json', '.html']
    
    def read_file(self, file_path: str) -> Dict[str, Any]:
        """
        Read a file and extract its content
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary containing file metadata and content
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.suffix not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {path.suffix}")
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse based on file type
        if path.suffix == '.md':
            html_content = markdown.markdown(content)
            parsed_content = content  # Keep original markdown
        elif path.suffix == '.json':
            parsed_content = json.loads(content)
        else:
            parsed_content = content
        
        return {
            'path': str(path.absolute()),
            'name': path.name,
            'type': path.suffix[1:],
            'content': parsed_content,
            'size': path.stat().st_size
        }
    
    def read_text(self, text: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process raw text input
        
        Args:
            text: Raw text content
            metadata: Optional metadata dictionary
            
        Returns:
            Dictionary containing content and metadata
        """
        if metadata is None:
            metadata = {}
        
        return {
            'path': metadata.get('path', 'text_input'),
            'name': metadata.get('name', 'Text Input'),
            'type': 'text',
            'content': text,
            'size': len(text)
        }
    
    def batch_read(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Read multiple files at once
        
        Args:
            file_paths: List of file paths
            
        Returns:
            List of document dictionaries
        """
        documents = []
        for path in file_paths:
            try:
                doc = self.read_file(path)
                documents.append(doc)
            except Exception as e:
                print(f"Error reading {path}: {e}")
        
        return documents
