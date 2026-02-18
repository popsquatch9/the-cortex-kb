#!/usr/bin/env python3
"""
Cortex Knowledge Base CLI
Command-line interface for interacting with the knowledge base
"""

import sys
import argparse
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from cortex.cortex import CortexKB


def main():
    parser = argparse.ArgumentParser(
        description='Cortex Knowledge Base - Smart Personal Knowledge Management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add a document to the knowledge base
  python cortex_cli.py add document.md
  
  # Add text directly
  python cortex_cli.py add-text "Machine learning is a subset of AI"
  
  # Search the knowledge base
  python cortex_cli.py search "machine learning"
  
  # Show statistics
  python cortex_cli.py stats
  
  # List all documents
  python cortex_cli.py list
  
  # Organize by category
  python cortex_cli.py organize
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Add document command
    add_parser = subparsers.add_parser('add', help='Add a document to the knowledge base')
    add_parser.add_argument('file', help='Path to the document file')
    add_parser.add_argument('--no-discovery', action='store_true', 
                           help='Disable external source discovery')
    
    # Add text command
    add_text_parser = subparsers.add_parser('add-text', help='Add text directly to the knowledge base')
    add_text_parser.add_argument('text', help='Text content to add')
    add_text_parser.add_argument('--name', help='Name for the text entry')
    add_text_parser.add_argument('--no-discovery', action='store_true',
                                help='Disable external source discovery')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search the knowledge base')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('-k', '--top-k', type=int, default=5,
                             help='Number of results to return (default: 5)')
    
    # Get document command
    get_parser = subparsers.add_parser('get', help='Get a document by ID')
    get_parser.add_argument('doc_id', help='Document ID')
    
    # Related documents command
    related_parser = subparsers.add_parser('related', help='Get related documents')
    related_parser.add_argument('doc_id', help='Document ID')
    
    # Statistics command
    subparsers.add_parser('stats', help='Show knowledge base statistics')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all documents')
    list_parser.add_argument('--category', help='Filter by category')
    
    # Organize command
    subparsers.add_parser('organize', help='Show documents organized by category')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize Cortex KB
    data_dir = os.getenv('DATA_DIR', './cortex_data')
    enable_discovery = os.getenv('ENABLE_WEB_SEARCH', 'true').lower() == 'true'
    threshold = float(os.getenv('RELEVANCE_THRESHOLD', '0.7'))
    
    cortex = CortexKB(
        storage_path=data_dir,
        enable_external_sources=enable_discovery,
        relevance_threshold=threshold
    )
    
    # Execute command
    if args.command == 'add':
        doc_id = cortex.add_document(args.file, discover_sources=not args.no_discovery)
        print(f"✓ Document added successfully!")
        print(f"  ID: {doc_id}")
        
        doc = cortex.get_document(doc_id)
        if doc:
            print(f"  Name: {doc.get('name')}")
            print(f"  Category: {doc.get('category')}")
            print(f"  Concepts: {', '.join(doc.get('concepts', [])[:5])}")
    
    elif args.command == 'add-text':
        metadata = {}
        if args.name:
            metadata['name'] = args.name
        
        doc_id = cortex.add_text(args.text, metadata, discover_sources=not args.no_discovery)
        print(f"✓ Text added successfully!")
        print(f"  ID: {doc_id}")
        
        doc = cortex.get_document(doc_id)
        if doc:
            print(f"  Category: {doc.get('category')}")
            print(f"  Concepts: {', '.join(doc.get('concepts', [])[:5])}")
    
    elif args.command == 'search':
        results = cortex.search(args.query, top_k=args.top_k)
        
        if not results:
            print("No results found.")
        else:
            print(f"Found {len(results)} result(s):\n")
            for i, doc in enumerate(results, 1):
                print(f"{i}. {doc.get('name', 'Untitled')} (similarity: {doc.get('similarity', 0):.2f})")
                print(f"   ID: {doc.get('id')}")
                print(f"   Category: {doc.get('category', 'unknown')}")
                content = str(doc.get('content', ''))
                preview = content[:100] + '...' if len(content) > 100 else content
                print(f"   Preview: {preview}")
                print()
    
    elif args.command == 'get':
        doc = cortex.get_document(args.doc_id)
        if not doc:
            print(f"Document not found: {args.doc_id}")
        else:
            print(f"Document: {doc.get('name', 'Untitled')}")
            print(f"ID: {doc.get('id')}")
            print(f"Type: {doc.get('type')}")
            print(f"Category: {doc.get('category', 'unknown')}")
            print(f"Concepts: {', '.join(doc.get('concepts', []))}")
            print(f"\nContent:\n{doc.get('content')}")
    
    elif args.command == 'related':
        related = cortex.get_related_documents(args.doc_id)
        
        if not related:
            print("No related documents found.")
        else:
            print(f"Found {len(related)} related document(s):\n")
            for i, doc in enumerate(related, 1):
                print(f"{i}. {doc.get('name', 'Untitled')}")
                print(f"   ID: {doc.get('id')}")
                print(f"   Category: {doc.get('category', 'unknown')}")
                print()
    
    elif args.command == 'stats':
        stats = cortex.get_statistics()
        
        print("Knowledge Base Statistics:")
        print(f"  Total nodes: {stats['total_nodes']}")
        print(f"  Total relationships: {stats['total_edges']}")
        print(f"\nNode types:")
        for node_type, count in stats['node_types'].items():
            print(f"  {node_type}: {count}")
        
        if stats['relationship_types']:
            print(f"\nRelationship types:")
            for rel_type, count in stats['relationship_types'].items():
                print(f"  {rel_type}: {count}")
    
    elif args.command == 'list':
        all_docs = cortex.graph.get_all_nodes()
        
        if args.category:
            all_docs = [doc for doc in all_docs if doc.get('category') == args.category]
        
        if not all_docs:
            print("No documents found.")
        else:
            print(f"Total documents: {len(all_docs)}\n")
            for i, doc in enumerate(all_docs, 1):
                print(f"{i}. {doc.get('name', 'Untitled')}")
                print(f"   ID: {doc.get('id')}")
                print(f"   Category: {doc.get('category', 'unknown')}")
                print(f"   Type: {doc.get('type')}")
                print()
    
    elif args.command == 'organize':
        organized = cortex.organize_by_category()
        
        print("Documents organized by category:\n")
        for category, docs in sorted(organized.items()):
            print(f"{category.upper()} ({len(docs)} documents):")
            for doc in docs:
                print(f"  - {doc.get('name', 'Untitled')} (ID: {doc.get('id')[:8]}...)")
            print()


if __name__ == '__main__':
    main()
