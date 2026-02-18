# Quick Start Guide

Get started with Cortex Knowledge Base in 5 minutes!

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/popsquatch9/the-cortex-kb.git
cd the-cortex-kb
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Verify installation**
```bash
python cortex_cli.py --help
```

## Your First Knowledge Base

### Step 1: Add Your First Document

Create a simple markdown file:
```bash
echo "# My First Note

Machine learning is transforming AI.

Learn more at https://en.wikipedia.org/wiki/Machine_learning" > my_note.md
```

Add it to your knowledge base:
```bash
python cortex_cli.py add my_note.md
```

### Step 2: Add Some Text

```bash
python cortex_cli.py add-text "Python is a great programming language" --name "Python Note"
```

### Step 3: Search Your Knowledge

```bash
python cortex_cli.py search "machine learning"
```

### Step 4: Explore Relationships

Get the document ID from the search results, then:
```bash
python cortex_cli.py related <doc_id>
```

### Step 5: Organize Your Knowledge

```bash
python cortex_cli.py organize
```

## Try the Demo

Run the full feature demonstration:
```bash
./demo.sh
```

## What's Next?

- Add more documents to build your knowledge base
- Experiment with semantic search
- Explore the automatic categorization
- Check out the example documents in the `examples/` folder
- Read the full [README.md](README.md) for detailed documentation

## Tips

1. **Use meaningful names** when adding text directly
2. **Let it discover sources** by including URLs in your documents
3. **Search semantically** - try queries like "AI learning" instead of exact text
4. **Browse by category** to see how content is organized
5. **Check statistics** regularly to track your knowledge growth

## Need Help?

- Run any command with `--help` for detailed usage
- Check the [README.md](README.md) for comprehensive documentation
- See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for technical details

Happy knowledge building! 🧠
