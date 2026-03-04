# The Cortex Knowledge Base

A smart personal knowledge base that reads, reasons, understands, and organizes information. Cortex automatically discovers related external sources and builds a carefully vetted, intuitively organized personal database.

> **📌 How to Launch?** This is a **Python CLI application**, not a web app. 
> - ❌ **GitHub Pages won't work** (it's for static websites only)
> - ✅ **Use local install or Docker** - See [HOW_TO_LAUNCH.md](HOW_TO_LAUNCH.md) for all options
> - ✅ **Quick start**: Run `./install.sh` or see [DEPLOYMENT.md](DEPLOYMENT.md)
> 
> **💾 Is data persistent?** YES! All installations save data permanently to disk.
> 
> **☁️ Is cloud deployment easy?** YES! One-command setup - see [CLOUD_DEPLOY.md](CLOUD_DEPLOY.md)

## Features

- **Intelligent Ingestion**: Reads and processes multiple document formats (Markdown, JSON, TXT, HTML)
- **Semantic Understanding**: Uses AI-powered semantic search to understand content meaning, not just keywords
- **Automatic Organization**: Categorizes content automatically and extracts key concepts
- **Knowledge Graph**: Maintains relationships between documents for intuitive navigation
- **Source Discovery**: Automatically finds and fetches relevant external sources from URLs in your documents
- **Quality Vetting**: Evaluates external sources for quality and relevance
- **Semantic Search**: Find related content based on meaning, not just text matching

## Quick Installation

### One-Command Install (Recommended)

```bash
git clone https://github.com/popsquatch9/the-cortex-kb.git
cd the-cortex-kb
./install.sh
```

### Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/popsquatch9/the-cortex-kb.git
cd the-cortex-kb
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Configure settings:
```bash
cp .env.example .env
# Edit .env to customize settings
```

### Docker Installation

```bash
docker build -t cortex-kb .
docker run -it -v $(pwd)/cortex_data:/app/cortex_data cortex-kb
```

### pip Install (From Source)

```bash
pip install -e .
cortex --help  # Now available system-wide
```

## Quick Start

### Adding Documents

Add a markdown file to your knowledge base:
```bash
python cortex_cli.py add document.md
```

Add text directly:
```bash
python cortex_cli.py add-text "Machine learning is a branch of artificial intelligence"
```

### Searching

Search for content using semantic search:
```bash
python cortex_cli.py search "artificial intelligence"
```

### Viewing Statistics

See what's in your knowledge base:
```bash
python cortex_cli.py stats
```

### Organizing Content

View documents organized by category:
```bash
python cortex_cli.py organize
```

## Usage Guide

### Command Line Interface

The Cortex CLI provides several commands:

#### `add` - Add a Document
```bash
python cortex_cli.py add <file_path> [--no-discovery]
```
Adds a document to the knowledge base. By default, it will:
- Parse the document content
- Extract key concepts
- Categorize the content
- Find related existing documents
- Discover and fetch external sources from URLs in the document

Use `--no-discovery` to skip external source discovery.

#### `add-text` - Add Text Directly
```bash
python cortex_cli.py add-text "<text>" [--name <name>] [--no-discovery]
```
Adds raw text to the knowledge base with optional name.

#### `search` - Semantic Search
```bash
python cortex_cli.py search "<query>" [-k <number>]
```
Searches the knowledge base using semantic similarity. Returns documents most similar to your query, even if they don't contain exact keywords.

#### `get` - Get Document by ID
```bash
python cortex_cli.py get <doc_id>
```
Retrieves a specific document by its ID.

#### `related` - Find Related Documents
```bash
python cortex_cli.py related <doc_id>
```
Shows all documents related to a given document.

#### `list` - List All Documents
```bash
python cortex_cli.py list [--category <category>]
```
Lists all documents, optionally filtered by category.

#### `organize` - View by Category
```bash
python cortex_cli.py organize
```
Shows all documents organized by their automatically assigned categories.

#### `stats` - Show Statistics
```bash
python cortex_cli.py stats
```
Displays statistics about your knowledge base including node counts, types, and relationships.

### Python API

You can also use Cortex programmatically:

```python
from cortex.cortex import CortexKB

# Initialize
cortex = CortexKB(storage_path="./my_knowledge_base")

# Add content
doc_id = cortex.add_document("article.md")

# Search
results = cortex.search("artificial intelligence", top_k=5)

# Get related documents
related = cortex.get_related_documents(doc_id)

# Get statistics
stats = cortex.get_statistics()
```

## How It Works

### 1. Document Ingestion
When you add a document, Cortex:
- Parses the content based on file type
- Extracts metadata (name, type, size)
- Stores it in the knowledge graph

### 2. Understanding and Reasoning
Cortex uses semantic embeddings to:
- Understand the meaning of content
- Extract key concepts
- Automatically categorize documents
- Compute semantic similarity between documents

### 3. Relationship Building
Cortex automatically:
- Finds related documents based on semantic similarity
- Creates relationship edges in the knowledge graph
- Maintains relevance scores for each relationship

### 4. External Source Discovery
For each document, Cortex:
- Extracts URLs from the content
- Fetches content from those URLs
- Vets sources for quality (domain reputation, content length, etc.)
- Links high-quality sources to the parent document

### 5. Intuitive Organization
Documents are:
- Automatically categorized (programming, research, notes, data, general)
- Tagged with key concepts
- Connected to related documents
- Organized in an easily navigable graph structure

## Deployment Options

**Important**: Cortex is a Python CLI application, **not a web application**. GitHub Pages is for static websites and **cannot host Python apps**.

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment guide including:
- **Local Installation**: Run on your personal computer
- **Docker**: Containerized deployment
- **Cloud Deployment**: Deploy to VPS or cloud instances
- **PyPI Package**: Install with pip (future)

Quick deploy options:
```bash
# Local with virtual environment
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Docker
docker-compose up -d

# System-wide install
pip install -e .
```

## Configuration

Create a `.env` file based on `.env.example`:

```bash
# Data storage location
DATA_DIR=./cortex_data

# Enable/disable external source discovery
ENABLE_WEB_SEARCH=true

# Maximum number of external sources per document
MAX_EXTERNAL_SOURCES=5

# Semantic embedding model
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Minimum relevance threshold (0.0 - 1.0)
RELEVANCE_THRESHOLD=0.7
```

## Architecture

Cortex consists of several modular components:

- **DocumentIngester**: Reads and parses various file formats
- **KnowledgeGraph**: Manages the graph structure of documents and relationships
- **SemanticEngine**: Provides AI-powered semantic understanding and search
- **SourceDiscovery**: Finds and fetches external sources
- **CortexKB**: Main orchestrator that ties all components together

## Data Storage

Cortex stores data in JSON files in the configured data directory:
- `nodes.json`: All documents and their metadata
- `edges.json`: Relationships between documents

## Supported File Formats

- Markdown (`.md`)
- Plain text (`.txt`)
- JSON (`.json`)
- HTML (`.html`)

## Requirements

See `requirements.txt` for full dependencies. Key packages:
- `sentence-transformers`: For semantic embeddings
- `beautifulsoup4`: For parsing HTML content
- `markdown`: For parsing Markdown files
- `requests`: For fetching external sources

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

MIT License - See LICENSE file for details

## Roadmap

Future enhancements planned:
- [ ] Web search API integration
- [ ] PDF support
- [ ] Image and multimedia support
- [ ] Advanced NLP for entity extraction
- [ ] Web UI interface
- [ ] Export functionality
- [ ] Collaborative features
- [ ] Cloud sync
- [ ] Mobile app
