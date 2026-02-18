#!/bin/bash
# Demonstration script for Cortex Knowledge Base
# This script showcases the main features of the system

echo "=========================================="
echo "Cortex Knowledge Base - Feature Demo"
echo "=========================================="
echo ""

# Clean up any existing demo data
echo "Cleaning up previous demo data..."
rm -rf ./demo_data
mkdir -p ./demo_data

# Set environment for demo
export DATA_DIR=./demo_data
export ENABLE_WEB_SEARCH=true
export RELEVANCE_THRESHOLD=0.7

echo "✓ Demo environment initialized"
echo ""

# 1. Add documents
echo "=========================================="
echo "1. ADDING DOCUMENTS TO KNOWLEDGE BASE"
echo "=========================================="
echo ""

echo "Adding machine learning document..."
python cortex_cli.py add examples/machine_learning.md --no-discovery
echo ""

echo "Adding Python programming notes..."
python cortex_cli.py add examples/python_notes.md --no-discovery
echo ""

echo "Adding data science notes..."
python cortex_cli.py add examples/data_science.md --no-discovery
echo ""

# 2. Add text directly
echo "=========================================="
echo "2. ADDING TEXT DIRECTLY"
echo "=========================================="
echo ""

echo "Adding a note about AI..."
python cortex_cli.py add-text "Artificial intelligence is revolutionizing technology. Neural networks can learn complex patterns from data." --name "AI Overview" --no-discovery
echo ""

# 3. Show statistics
echo "=========================================="
echo "3. KNOWLEDGE BASE STATISTICS"
echo "=========================================="
echo ""
python cortex_cli.py stats
echo ""

# 4. List all documents
echo "=========================================="
echo "4. LISTING ALL DOCUMENTS"
echo "=========================================="
echo ""
python cortex_cli.py list
echo ""

# 5. Organize by category
echo "=========================================="
echo "5. ORGANIZING BY CATEGORY"
echo "=========================================="
echo ""
python cortex_cli.py organize
echo ""

# 6. Search for content
echo "=========================================="
echo "6. SEMANTIC SEARCH"
echo "=========================================="
echo ""

echo "Searching for 'machine learning algorithms'..."
python cortex_cli.py search "machine learning algorithms" -k 3
echo ""

echo "Searching for 'python programming'..."
python cortex_cli.py search "python programming" -k 2
echo ""

# 7. Show related documents
echo "=========================================="
echo "7. FINDING RELATED DOCUMENTS"
echo "=========================================="
echo ""

# Get the first document ID
DOC_ID=$(python -c "
import sys
sys.path.insert(0, '.')
from cortex.cortex import CortexKB
cortex = CortexKB(storage_path='./demo_data', enable_external_sources=False)
docs = cortex.graph.get_all_nodes()
if docs:
    print(docs[0]['id'])
")

if [ ! -z "$DOC_ID" ]; then
    echo "Finding documents related to ID: $DOC_ID..."
    python cortex_cli.py related "$DOC_ID"
    echo ""
fi

# 8. Summary
echo "=========================================="
echo "8. DEMO SUMMARY"
echo "=========================================="
echo ""
echo "✓ Successfully demonstrated:"
echo "  - Document ingestion from files"
echo "  - Direct text input"
echo "  - Automatic categorization"
echo "  - Knowledge graph with relationships"
echo "  - Semantic search"
echo "  - Document organization"
echo "  - Related document discovery"
echo ""
echo "The Cortex Knowledge Base is ready to use!"
echo ""
echo "Key Features:"
echo "  • Reads multiple file formats (MD, TXT, JSON, HTML)"
echo "  • Understands content semantically"
echo "  • Automatically categorizes and organizes"
echo "  • Discovers relationships between documents"
echo "  • Can fetch and vet external sources (when enabled)"
echo "  • Provides intuitive CLI interface"
echo ""
echo "For more information, see the README.md"
echo "=========================================="
