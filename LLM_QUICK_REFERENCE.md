# LLM Quick Reference

Quick reference for using Anthropic Claude and Google Gemini with Cortex KB.

## Setup (One-Time)

### Option 1: Anthropic Claude
```bash
# 1. Get API key from https://console.anthropic.com/
# 2. Add to .env file:
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-your-api-key-here

# 3. Install
pip install anthropic
```

### Option 2: Google Gemini
```bash
# 1. Get API key from https://makersuite.google.com/app/apikey
# 2. Add to .env file:
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your-google-api-key-here

# 3. Install
pip install google-generativeai
```

## Commands

### Ask Questions
```bash
# Ask about entire knowledge base
python cortex_cli.py ask "What are the main topics I've documented?"

# Ask about specific document
python cortex_cli.py ask "What is the key insight here?" --doc-id <doc_id>
```

### Summarize Documents
```bash
# Default 200-word summary
python cortex_cli.py summarize <doc_id>

# Custom length
python cortex_cli.py summarize <doc_id> --length 500
```

### Get AI Insights
```bash
# Generate insights about a document
python cortex_cli.py insights <doc_id>
```

### Regular Commands (Enhanced with LLM)
```bash
# Add document (gets better categorization with LLM)
python cortex_cli.py add document.md

# Add text (gets better categorization with LLM)
python cortex_cli.py add-text "Your content here" --name "My Note"

# Search (same as before)
python cortex_cli.py search "query"

# List documents (same as before)
python cortex_cli.py list
```

## Model Selection

### Claude Models (in .env)
```bash
CLAUDE_MODEL=claude-3-5-sonnet-20241022  # Default, latest
# CLAUDE_MODEL=claude-3-opus-20240229    # Most powerful
# CLAUDE_MODEL=claude-3-haiku-20240307   # Fastest, cheapest
```

### Gemini Models (in .env)
```bash
GEMINI_MODEL=gemini-pro  # Default
# GEMINI_MODEL=gemini-1.5-pro  # Latest version
# GEMINI_MODEL=gemini-pro-vision  # Supports images
```

## Programmatic Usage

### Python API
```python
from cortex.cortex import CortexKB

# Initialize with LLM
cortex = CortexKB(llm_provider='claude')

# Add document
doc_id = cortex.add_document('document.md')

# Ask question
answer = cortex.ask_question("What is this about?", doc_id)
print(answer)

# Summarize
summary = cortex.summarize_document(doc_id, max_length=200)
print(summary)

# Get insights
insights = cortex.get_insights(doc_id)
print(insights)
```

### Direct LLM Client
```python
from cortex.llm_provider import LLMClient

# Initialize
llm = LLMClient(provider='claude')

# Summarize
summary = llm.summarize("Long text here...", max_length=100)

# Answer question
answer = llm.answer_question("Question?", "Context here...")

# Generate insights
insights = llm.generate_insights("Text to analyze...")

# Categorize
category = llm.categorize("Text to categorize...")

# Extract concepts
concepts = llm.extract_key_concepts("Text here...")
```

## Troubleshooting

### "No LLM provider configured"
```bash
# Check .env file exists
ls -la .env

# Check it has correct settings
cat .env | grep LLM_PROVIDER
cat .env | grep API_KEY
```

### "Module not found: anthropic"
```bash
pip install anthropic
```

### "Module not found: google.generativeai"
```bash
pip install google-generativeai
```

### "API key not found"
```bash
# Make sure .env file is in project root
# API key should not have quotes:
ANTHROPIC_API_KEY=sk-ant-key-here  # ✓ Correct
ANTHROPIC_API_KEY="sk-ant-key-here"  # ✗ Wrong (remove quotes)
```

### Test Without LLM
```bash
# Set provider to none in .env
LLM_PROVIDER=none

# Or unset it
# LLM_PROVIDER=
```

## Cost Estimates

### Anthropic Claude
- Claude 3.5 Sonnet: ~$3/$15 per million tokens (input/output)
- Claude 3 Haiku: ~$0.25/$1.25 per million tokens
- Typical document: ~500-1000 tokens
- Typical summary: ~200 tokens

### Google Gemini
- Free tier: 60 requests/minute
- Paid tier: Pay as you go
- Generally cheaper than Claude for light use

## Tips

- Start with Gemini free tier to test
- Use Claude for complex analysis
- Use `--length` to control summary size
- Ask specific questions for better answers
- Fallback mode works offline (no LLM needed)

## More Info

- **Full Guide**: [LLM_INTEGRATION.md](LLM_INTEGRATION.md)
- **Demo**: Run `python3 demo_llm.py`
- **Documentation**: [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
