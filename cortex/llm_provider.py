"""
LLM Provider Module
Unified interface for Anthropic Claude and Google Gemini APIs
"""

import os
from typing import Optional, Dict, Any, List
from enum import Enum


class LLMProvider(Enum):
    """Available LLM providers"""
    CLAUDE = "claude"
    GEMINI = "gemini"
    NONE = "none"


class LLMClient:
    """
    Unified LLM client supporting Anthropic Claude and Google Gemini
    """
    
    def __init__(
        self, 
        provider: str = "none",
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        """
        Initialize LLM client
        
        Args:
            provider: LLM provider to use ('claude', 'gemini', or 'none')
            api_key: API key for the provider (or use environment variable)
            model: Specific model to use (optional, uses defaults)
        """
        self.provider = LLMProvider(provider.lower())
        self.api_key = api_key
        self.model = model
        self.client = None
        
        # Initialize the appropriate client
        if self.provider == LLMProvider.CLAUDE:
            self._init_claude()
        elif self.provider == LLMProvider.GEMINI:
            self._init_gemini()
    
    def _init_claude(self):
        """Initialize Anthropic Claude client"""
        try:
            import anthropic
            
            # Get API key from parameter or environment
            key = self.api_key or os.getenv('ANTHROPIC_API_KEY')
            if not key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment or parameters")
            
            self.client = anthropic.Anthropic(api_key=key)
            
            # Set default model if not specified
            if not self.model:
                self.model = "claude-3-5-sonnet-20241022"  # Latest Claude model
                
            print(f"✓ Initialized Anthropic Claude with model: {self.model}")
            
        except ImportError:
            raise ImportError(
                "Anthropic library not installed. "
                "Install with: pip install anthropic"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Claude: {e}")
    
    def _init_gemini(self):
        """Initialize Google Gemini client"""
        try:
            import google.generativeai as genai
            
            # Get API key from parameter or environment
            key = self.api_key or os.getenv('GOOGLE_API_KEY')
            if not key:
                raise ValueError("GOOGLE_API_KEY not found in environment or parameters")
            
            genai.configure(api_key=key)
            
            # Set default model if not specified
            if not self.model:
                self.model = "gemini-pro"
            
            self.client = genai.GenerativeModel(self.model)
            
            print(f"✓ Initialized Google Gemini with model: {self.model}")
            
        except ImportError:
            raise ImportError(
                "Google Generative AI library not installed. "
                "Install with: pip install google-generativeai"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Gemini: {e}")
    
    def is_available(self) -> bool:
        """Check if LLM is available"""
        return self.provider != LLMProvider.NONE and self.client is not None
    
    def generate(
        self, 
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.7
    ) -> str:
        """
        Generate text using the LLM
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (for Claude)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 - 1.0)
            
        Returns:
            Generated text
        """
        if not self.is_available():
            raise RuntimeError("No LLM provider configured")
        
        if self.provider == LLMProvider.CLAUDE:
            return self._generate_claude(prompt, system_prompt, max_tokens, temperature)
        elif self.provider == LLMProvider.GEMINI:
            return self._generate_gemini(prompt, max_tokens, temperature)
        
        return ""
    
    def _generate_claude(
        self, 
        prompt: str,
        system_prompt: Optional[str],
        max_tokens: int,
        temperature: float
    ) -> str:
        """Generate using Claude"""
        try:
            messages = [{"role": "user", "content": prompt}]
            
            kwargs = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": messages
            }
            
            if system_prompt:
                kwargs["system"] = system_prompt
            
            response = self.client.messages.create(**kwargs)
            return response.content[0].text
            
        except Exception as e:
            raise RuntimeError(f"Claude generation failed: {e}")
    
    def _generate_gemini(
        self,
        prompt: str,
        max_tokens: int,
        temperature: float
    ) -> str:
        """Generate using Gemini"""
        try:
            generation_config = {
                "max_output_tokens": max_tokens,
                "temperature": temperature,
            }
            
            response = self.client.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
            
        except Exception as e:
            raise RuntimeError(f"Gemini generation failed: {e}")
    
    def summarize(self, text: str, max_length: int = 200) -> str:
        """
        Summarize text using the LLM
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary in words
            
        Returns:
            Summary text
        """
        if not self.is_available():
            # Fallback to simple truncation
            words = text.split()
            if len(words) <= max_length:
                return text
            return ' '.join(words[:max_length]) + '...'
        
        prompt = f"""Summarize the following text in {max_length} words or less. 
Focus on the key points and main ideas.

Text:
{text}

Summary:"""
        
        return self.generate(
            prompt=prompt,
            system_prompt="You are a helpful assistant that creates concise, accurate summaries.",
            max_tokens=max_length * 2,  # Roughly 2 tokens per word
            temperature=0.3  # Lower temperature for more focused summaries
        )
    
    def categorize(self, text: str, categories: Optional[List[str]] = None) -> str:
        """
        Categorize text using the LLM
        
        Args:
            text: Text to categorize
            categories: Optional list of valid categories
            
        Returns:
            Category name
        """
        if not self.is_available():
            # Fallback to simple categorization
            text_lower = text.lower()
            if any(word in text_lower for word in ['code', 'programming', 'function']):
                return 'programming'
            elif any(word in text_lower for word in ['research', 'study', 'paper']):
                return 'research'
            elif any(word in text_lower for word in ['note', 'memo', 'todo']):
                return 'notes'
            elif any(word in text_lower for word in ['data', 'analysis', 'statistics']):
                return 'data'
            return 'general'
        
        if categories:
            category_list = ', '.join(categories)
            prompt = f"""Categorize the following text into ONE of these categories: {category_list}

Text:
{text}

Category (respond with just the category name):"""
        else:
            prompt = f"""Categorize the following text into ONE category. Choose from: programming, research, notes, data, general, or suggest a better category.

Text:
{text}

Category (respond with just the category name):"""
        
        response = self.generate(
            prompt=prompt,
            system_prompt="You are a helpful assistant that categorizes text accurately.",
            max_tokens=50,
            temperature=0.2
        )
        
        return response.strip().lower()
    
    def extract_key_concepts(self, text: str, max_concepts: int = 10) -> List[str]:
        """
        Extract key concepts from text using the LLM
        
        Args:
            text: Text to analyze
            max_concepts: Maximum number of concepts to extract
            
        Returns:
            List of key concepts
        """
        if not self.is_available():
            # Fallback to simple extraction
            words = text.split()
            concepts = []
            for word in words:
                clean_word = ''.join(c for c in word if c.isalnum())
                if len(clean_word) > 4:
                    concepts.append(clean_word.lower())
            return list(set(concepts))[:max_concepts]
        
        prompt = f"""Extract up to {max_concepts} key concepts or topics from the following text.
Return them as a comma-separated list.

Text:
{text}

Key concepts (comma-separated):"""
        
        response = self.generate(
            prompt=prompt,
            system_prompt="You are a helpful assistant that extracts key concepts from text.",
            max_tokens=200,
            temperature=0.3
        )
        
        # Parse the response into a list
        concepts = [c.strip() for c in response.split(',')]
        return [c for c in concepts if c][:max_concepts]
    
    def answer_question(self, question: str, context: str) -> str:
        """
        Answer a question based on context using the LLM
        
        Args:
            question: Question to answer
            context: Context to use for answering
            
        Returns:
            Answer text
        """
        if not self.is_available():
            return "LLM not available for question answering. Please configure an API key."
        
        prompt = f"""Based on the following context, answer the question.
If the answer is not in the context, say "I don't have enough information to answer this question."

Context:
{context}

Question: {question}

Answer:"""
        
        return self.generate(
            prompt=prompt,
            system_prompt="You are a helpful assistant that answers questions based on provided context.",
            max_tokens=500,
            temperature=0.5
        )
    
    def generate_insights(self, text: str) -> str:
        """
        Generate insights about the text using the LLM
        
        Args:
            text: Text to analyze
            
        Returns:
            Insights text
        """
        if not self.is_available():
            return "LLM not available for generating insights."
        
        prompt = f"""Analyze the following text and provide 3-5 key insights or takeaways.

Text:
{text}

Key insights:"""
        
        return self.generate(
            prompt=prompt,
            system_prompt="You are a helpful assistant that analyzes text and provides valuable insights.",
            max_tokens=400,
            temperature=0.6
        )
