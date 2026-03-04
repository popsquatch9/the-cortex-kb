#!/usr/bin/env python3
"""
LLM Integration Demo
Demonstrates Anthropic Claude and Google Gemini integration
"""

import os
import sys

# Ensure we can import cortex modules
sys.path.insert(0, os.path.dirname(__file__))

from cortex.llm_provider import LLMClient


def demo_without_llm():
    """Demo fallback behavior without LLM"""
    print("=" * 70)
    print("DEMO 1: Without LLM (Fallback Mode)")
    print("=" * 70)
    
    llm = LLMClient(provider='none')
    
    print(f"\n✓ LLM Provider: {llm.provider.value}")
    print(f"✓ Available: {llm.is_available()}")
    
    # Test fallback categorization
    text = "Python code with functions, classes, and imports for data analysis"
    category = llm.categorize(text)
    print(f"\n📁 Categorization (fallback): {category}")
    
    # Test fallback concept extraction
    concepts = llm.extract_key_concepts(text)
    print(f"🔑 Key concepts (fallback): {concepts[:5]}")
    
    # Test fallback summarization
    long_text = "Artificial intelligence is transforming how we work. " * 50
    summary = llm.summarize(long_text, max_length=20)
    print(f"\n📝 Summary (fallback - first 100 chars): {summary[:100]}...")
    
    print("\n✓ Fallback mode works! (Local processing, no API needed)\n")


def demo_with_mock_claude():
    """Demo how Claude would work (without actual API key)"""
    print("=" * 70)
    print("DEMO 2: With Anthropic Claude (Mock Setup)")
    print("=" * 70)
    
    print("\n📚 How to use Claude:")
    print("   1. Get API key from: https://console.anthropic.com/")
    print("   2. Set in .env: LLM_PROVIDER=claude")
    print("   3. Set in .env: ANTHROPIC_API_KEY=sk-ant-your-key-here")
    print("   4. Install: pip install anthropic")
    
    print("\n🎯 Features with Claude:")
    print("   • Advanced document categorization")
    print("   • Intelligent concept extraction")
    print("   • High-quality summarization")
    print("   • Context-aware question answering")
    print("   • Deep insights generation")
    
    print("\n💡 Example usage:")
    print("   from cortex.llm_provider import LLMClient")
    print("   llm = LLMClient(provider='claude')")
    print("   summary = llm.summarize(document_text)")
    print("   answer = llm.answer_question(question, context)")
    
    print("\n📊 Claude Models:")
    print("   • claude-3-5-sonnet-20241022 (Default, Latest)")
    print("   • claude-3-opus-20240229 (Most Powerful)")
    print("   • claude-3-haiku-20240307 (Fastest)")
    
    print()


def demo_with_mock_gemini():
    """Demo how Gemini would work (without actual API key)"""
    print("=" * 70)
    print("DEMO 3: With Google Gemini (Mock Setup)")
    print("=" * 70)
    
    print("\n📚 How to use Gemini:")
    print("   1. Get API key from: https://makersuite.google.com/app/apikey")
    print("   2. Set in .env: LLM_PROVIDER=gemini")
    print("   3. Set in .env: GOOGLE_API_KEY=your-google-api-key-here")
    print("   4. Install: pip install google-generativeai")
    
    print("\n🎯 Features with Gemini:")
    print("   • Google Workspace integration")
    print("   • Free tier available")
    print("   • Multimodal support (text + images)")
    print("   • Advanced summarization")
    print("   • Question answering")
    
    print("\n💡 Example usage:")
    print("   from cortex.llm_provider import LLMClient")
    print("   llm = LLMClient(provider='gemini')")
    print("   insights = llm.generate_insights(document_text)")
    print("   category = llm.categorize(text)")
    
    print("\n📊 Gemini Models:")
    print("   • gemini-pro (Default, Best for text)")
    print("   • gemini-1.5-pro (Latest version)")
    print("   • gemini-pro-vision (Supports images)")
    
    print()


def demo_cli_usage():
    """Demo CLI commands"""
    print("=" * 70)
    print("DEMO 4: CLI Usage Examples")
    print("=" * 70)
    
    print("\n📝 Add a document:")
    print("   python cortex_cli.py add document.md")
    
    print("\n🔍 Search:")
    print("   python cortex_cli.py search 'machine learning'")
    
    print("\n❓ Ask a question (requires LLM):")
    print("   python cortex_cli.py ask 'What are the main topics?'")
    
    print("\n📄 Summarize a document (requires LLM):")
    print("   python cortex_cli.py summarize <doc_id> --length 200")
    
    print("\n✨ Get insights (requires LLM):")
    print("   python cortex_cli.py insights <doc_id>")
    
    print("\n📊 View statistics:")
    print("   python cortex_cli.py stats")
    
    print()


def demo_comparison():
    """Compare Claude vs Gemini"""
    print("=" * 70)
    print("DEMO 5: Claude vs Gemini Comparison")
    print("=" * 70)
    
    print("\n" + "=" * 70)
    print(f"{'Feature':<25} {'Claude':<22} {'Gemini':<22}")
    print("=" * 70)
    
    comparisons = [
        ("Quality", "Excellent", "Very Good"),
        ("Speed", "Fast", "Fast"),
        ("Context Window", "200k tokens", "32k tokens"),
        ("Cost", "Pay per use", "Free tier + paid"),
        ("Google Workspace", "No", "Yes ✓"),
        ("Multimodal", "Limited", "Yes (Vision)"),
        ("Best For", "Reasoning & Analysis", "Google Integration"),
    ]
    
    for feature, claude, gemini in comparisons:
        print(f"{feature:<25} {claude:<22} {gemini:<22}")
    
    print("=" * 70)
    
    print("\n💡 Recommendation:")
    print("   • Use Claude for: Advanced reasoning, long documents, high quality")
    print("   • Use Gemini for: Google Workspace, free tier, multimodal needs")
    
    print()


def main():
    """Run all demos"""
    print("\n" + "🧠" * 35)
    print("     Cortex KB - LLM Integration Demo")
    print("     Anthropic Claude & Google Gemini")
    print("🧠" * 35 + "\n")
    
    try:
        # Run demos
        demo_without_llm()
        input("Press Enter to continue...")
        
        demo_with_mock_claude()
        input("Press Enter to continue...")
        
        demo_with_mock_gemini()
        input("Press Enter to continue...")
        
        demo_cli_usage()
        input("Press Enter to continue...")
        
        demo_comparison()
        
        # Final notes
        print("=" * 70)
        print("✅ Demo Complete!")
        print("=" * 70)
        
        print("\n📖 Next Steps:")
        print("   1. Choose LLM provider (Claude or Gemini)")
        print("   2. Get API key")
        print("   3. Configure .env file")
        print("   4. Install dependencies")
        print("   5. Try the examples!")
        
        print("\n📚 Documentation:")
        print("   • LLM_INTEGRATION.md - Complete setup guide")
        print("   • README.md - Project overview")
        print("   • .env.example - Configuration template")
        
        print("\n🎉 Enjoy your AI-powered knowledge base!\n")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!\n")
        sys.exit(0)


if __name__ == '__main__':
    main()
