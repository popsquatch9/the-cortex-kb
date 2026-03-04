# LLM Integration Guide

Cortex KB now supports **Anthropic Claude** and **Google Gemini** APIs for enhanced AI capabilities!

## Quick Start

### 1. Choose Your LLM Provider

You can use either:
- **Anthropic Claude** - Recommended for high-quality reasoning and analysis
- **Google Gemini Pro** - Great integration with Google Workspace

### 2. Get Your API Key

#### For Anthropic Claude:
1. Visit https://console.anthropic.com/
2. Sign up for an account
3. Create an API key
4. Copy your API key

#### For Google Gemini:
1. Visit https://makersuite.google.com/app/apikey
2. Sign in with your Google Workspace account
3. Create an API key
4. Copy your API key

### 3. Configure Cortex

Edit your `.env` file (or create one from `.env.example`):

**For Claude:**
```bash
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

**For Gemini:**
```bash
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your-google-api-key-here
```

### 4. Install Dependencies

```bash
# For Claude
pip install anthropic

# For Gemini
pip install google-generativeai

# Or install both
pip install -r requirements.txt
```

## Features

With LLM integration, you get:

### 1. **Enhanced Categorization**
AI automatically categorizes your documents more accurately based on content understanding.

### 2. **Smart Concept Extraction**
Extracts key concepts and topics using AI, not just keyword matching.

### 3. **Document Summarization**
```bash
python cortex_cli.py summarize <doc_id>
```
Get AI-generated summaries of your documents.

### 4. **Question Answering**
```bash
# Ask about the entire knowledge base
python cortex_cli.py ask "What are the main topics in my knowledge base?"

# Ask about a specific document
python cortex_cli.py ask "What is this document about?" --doc-id <doc_id>
```

### 5. **AI Insights**
```bash
python cortex_cli.py insights <doc_id>
```
Get AI-generated insights and key takeaways from your documents.

## Usage Examples

### Example 1: Add a document with LLM-powered analysis
```bash
python cortex_cli.py add document.md
```
With LLM enabled, this will:
- Automatically categorize using AI
- Extract key concepts intelligently
- Generate better metadata

### Example 2: Ask questions about your knowledge
```bash
# General question
python cortex_cli.py ask "Summarize everything I know about machine learning"

# Question about specific document
python cortex_cli.py ask "What are the key points?" --doc-id abc123
```

### Example 3: Summarize a long document
```bash
# Default 200-word summary
python cortex_cli.py summarize abc123

# Custom length
python cortex_cli.py summarize abc123 --length 500
```

### Example 4: Get AI insights
```bash
python cortex_cli.py insights abc123
```

## Configuration Options

In your `.env` file:

```bash
# Choose provider: 'claude', 'gemini', or 'none'
LLM_PROVIDER=claude

# API Keys
ANTHROPIC_API_KEY=your-key-here
GOOGLE_API_KEY=your-key-here

# Optional: Specify models
CLAUDE_MODEL=claude-3-5-sonnet-20241022
GEMINI_MODEL=gemini-pro

# Enable/disable LLM features
LLM_SUMMARIZATION=true
LLM_CATEGORIZATION=true
LLM_CONCEPT_EXTRACTION=true
```

## Model Options

### Anthropic Claude Models
- `claude-3-5-sonnet-20241022` (Default) - Latest, most capable
- `claude-3-opus-20240229` - Most powerful, slower
- `claude-3-sonnet-20240229` - Balanced performance
- `claude-3-haiku-20240307` - Fastest, lower cost

### Google Gemini Models
- `gemini-pro` (Default) - Best for text
- `gemini-pro-vision` - Supports images
- `gemini-1.5-pro` - Latest version with longer context

## API Costs

### Anthropic Claude Pricing (as of 2024)
- Claude 3.5 Sonnet: $3 per million input tokens, $15 per million output tokens
- Claude 3 Haiku: $0.25 per million input tokens, $1.25 per million output tokens

### Google Gemini Pricing
- Gemini Pro: Free tier available with rate limits
- Pay-as-you-go available for higher usage

💡 **Tip**: Start with Gemini's free tier to test, then upgrade based on your needs.

## Fallback Behavior

If LLM is not configured or unavailable, Cortex KB will:
- ✅ Continue working with local sentence-transformers
- ✅ Use simple keyword-based categorization
- ✅ Use basic concept extraction
- ⚠️ Question answering and insights will not be available

## Troubleshooting

### "No LLM provider configured"
- Check that `LLM_PROVIDER` is set in `.env`
- Verify API key is correct
- Ensure dependencies are installed

### "API key not found"
- Check `.env` file exists in project root
- Verify `ANTHROPIC_API_KEY` or `GOOGLE_API_KEY` is set
- API keys must not have quotes in `.env` file

### "Module not found: anthropic"
```bash
pip install anthropic
```

### "Module not found: google.generativeai"
```bash
pip install google-generativeai
```

### Rate limits or quota errors
- Claude: Check your account limits at https://console.anthropic.com/
- Gemini: Check usage at https://makersuite.google.com/

## Privacy & Security

- API keys are stored locally in `.env` file
- Never commit `.env` to version control (it's in `.gitignore`)
- Your documents are sent to the LLM provider for processing
- Claude and Gemini have their own data retention policies

## Google Workspace Integration

If you have Google Workspace with Gemini Pro:
1. Use your Workspace account to get Gemini API access
2. Set `LLM_PROVIDER=gemini`
3. Add your Google API key
4. Enjoy seamless integration with your Google ecosystem!

## Comparison: Claude vs Gemini

| Feature | Anthropic Claude | Google Gemini |
|---------|-----------------|---------------|
| **Quality** | Excellent | Very Good |
| **Speed** | Fast | Fast |
| **Context Window** | 200k tokens | 32k tokens |
| **Cost** | Pay per use | Free tier + paid |
| **Google Workspace** | ❌ | ✅ Native |
| **Multimodal** | Limited | ✅ Vision support |

### When to use Claude:
- Need highest quality reasoning
- Working with very long documents
- Need nuanced understanding

### When to use Gemini:
- Have Google Workspace subscription
- Want free tier to start
- Need vision/image support
- Prefer Google ecosystem

## Next Steps

1. ✅ Choose your LLM provider
2. ✅ Get API key
3. ✅ Configure `.env`
4. ✅ Install dependencies
5. ✅ Try the examples above!

For more help, see:
- [README.md](README.md) - Project overview
- [QUICKSTART.md](QUICKSTART.md) - Basic usage
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - All documentation

Happy knowledge building with AI! 🧠✨
