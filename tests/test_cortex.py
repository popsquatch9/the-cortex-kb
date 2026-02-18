"""
Test suite for Cortex Knowledge Base
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cortex.ingestion import DocumentIngester
from cortex.knowledge_graph import KnowledgeGraph
from cortex.semantic_engine import SemanticEngine
from cortex.source_discovery import SourceDiscovery
from cortex.cortex import CortexKB


class TestDocumentIngester(unittest.TestCase):
    """Test document ingestion functionality"""
    
    def setUp(self):
        self.ingester = DocumentIngester()
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_read_text(self):
        """Test reading raw text"""
        text = "This is a test document"
        doc = self.ingester.read_text(text)
        
        self.assertEqual(doc['content'], text)
        self.assertEqual(doc['type'], 'text')
        self.assertIn('name', doc)
    
    def test_read_text_with_metadata(self):
        """Test reading text with metadata"""
        text = "Test content"
        metadata = {'name': 'Test Doc', 'author': 'Test'}
        doc = self.ingester.read_text(text, metadata)
        
        self.assertEqual(doc['name'], 'Test Doc')
    
    def test_supported_formats(self):
        """Test that supported formats are defined"""
        self.assertIn('.txt', self.ingester.supported_formats)
        self.assertIn('.md', self.ingester.supported_formats)
        self.assertIn('.json', self.ingester.supported_formats)


class TestKnowledgeGraph(unittest.TestCase):
    """Test knowledge graph functionality"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.graph = KnowledgeGraph(self.test_dir)
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_add_node(self):
        """Test adding a node"""
        node_id = self.graph.add_node('test1', {'content': 'Test content'})
        self.assertEqual(node_id, 'test1')
        
        node = self.graph.get_node('test1')
        self.assertIsNotNone(node)
        self.assertEqual(node['content'], 'Test content')
    
    def test_add_edge(self):
        """Test adding an edge"""
        self.graph.add_node('node1', {'content': 'Node 1'})
        self.graph.add_node('node2', {'content': 'Node 2'})
        
        self.graph.add_edge('node1', 'node2', 'related_to', 0.8)
        
        related = self.graph.get_related_nodes('node1')
        self.assertEqual(len(related), 1)
        self.assertEqual(related[0]['id'], 'node2')
    
    def test_search_nodes(self):
        """Test searching nodes"""
        self.graph.add_node('doc1', {'content': 'Machine learning basics'})
        self.graph.add_node('doc2', {'content': 'Python programming'})
        
        results = self.graph.search_nodes('machine')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], 'doc1')
    
    def test_statistics(self):
        """Test getting statistics"""
        self.graph.add_node('doc1', {'content': 'Test', 'type': 'text'})
        self.graph.add_node('doc2', {'content': 'Test', 'type': 'text'})
        
        stats = self.graph.get_statistics()
        self.assertEqual(stats['total_nodes'], 2)
        self.assertEqual(stats['total_edges'], 0)


class TestSemanticEngine(unittest.TestCase):
    """Test semantic engine functionality"""
    
    def setUp(self):
        # Use a lightweight model for testing
        self.engine = SemanticEngine()
    
    def test_embed_text(self):
        """Test text embedding"""
        text = "Machine learning is great"
        embedding = self.engine.embed_text(text)
        
        self.assertIsNotNone(embedding)
        self.assertTrue(len(embedding) > 0)
    
    def test_compute_similarity(self):
        """Test similarity computation"""
        text1 = "Machine learning algorithms"
        text2 = "Machine learning models"
        text3 = "Cooking recipes"
        
        # Similar texts should have high similarity
        sim1 = self.engine.compute_similarity(text1, text2)
        self.assertGreater(sim1, 0.7)
        
        # Dissimilar texts should have lower similarity
        sim2 = self.engine.compute_similarity(text1, text3)
        self.assertLess(sim2, sim1)
    
    def test_extract_key_concepts(self):
        """Test key concept extraction"""
        text = "Machine learning and artificial intelligence are transforming technology"
        concepts = self.engine.extract_key_concepts(text)
        
        self.assertIsInstance(concepts, list)
        self.assertTrue(len(concepts) > 0)
    
    def test_categorize_content(self):
        """Test content categorization"""
        code_text = "def function(): import numpy as np"
        research_text = "This research paper studies the effects"
        
        code_cat = self.engine.categorize_content(code_text)
        research_cat = self.engine.categorize_content(research_text)
        
        self.assertEqual(code_cat, 'programming')
        self.assertEqual(research_cat, 'research')


class TestSourceDiscovery(unittest.TestCase):
    """Test source discovery functionality"""
    
    def setUp(self):
        self.discovery = SourceDiscovery()
    
    def test_extract_urls(self):
        """Test URL extraction"""
        text = "Check out https://example.com and http://test.org for more info"
        urls = self.discovery.extract_urls_from_text(text)
        
        self.assertEqual(len(urls), 2)
        self.assertIn('https://example.com', urls)
        self.assertIn('http://test.org', urls)
    
    def test_vet_source(self):
        """Test source vetting"""
        source = {
            'url': 'https://example.edu',
            'content': 'A' * 2000,
            'title': 'Educational Article'
        }
        
        vetted = self.discovery.vet_source(source)
        
        self.assertIn('quality_score', vetted)
        self.assertTrue(vetted['vetted'])
        self.assertGreater(vetted['quality_score'], 0.5)


class TestCortexKB(unittest.TestCase):
    """Test main Cortex KB functionality"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.cortex = CortexKB(
            storage_path=self.test_dir,
            enable_external_sources=False
        )
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_add_text(self):
        """Test adding text to knowledge base"""
        doc_id = self.cortex.add_text("Machine learning is fascinating", discover_sources=False)
        
        self.assertIsNotNone(doc_id)
        
        doc = self.cortex.get_document(doc_id)
        self.assertIsNotNone(doc)
        self.assertIn('category', doc)
        self.assertIn('concepts', doc)
    
    def test_search(self):
        """Test semantic search"""
        self.cortex.add_text("Artificial intelligence and machine learning", discover_sources=False)
        self.cortex.add_text("Cooking pasta recipes", discover_sources=False)
        
        results = self.cortex.search("AI and ML")
        
        self.assertGreater(len(results), 0)
        # First result should be about AI/ML
        self.assertIn('intelligence', results[0]['content'].lower())
    
    def test_get_statistics(self):
        """Test getting statistics"""
        self.cortex.add_text("Test document 1", discover_sources=False)
        self.cortex.add_text("Test document 2", discover_sources=False)
        
        stats = self.cortex.get_statistics()
        
        self.assertGreaterEqual(stats['total_nodes'], 2)
        self.assertIn('node_types', stats)
    
    def test_organize_by_category(self):
        """Test organization by category"""
        self.cortex.add_text("import numpy as np", discover_sources=False)
        self.cortex.add_text("Research paper abstract", discover_sources=False)
        
        organized = self.cortex.organize_by_category()
        
        self.assertIsInstance(organized, dict)
        self.assertGreater(len(organized), 0)


if __name__ == '__main__':
    unittest.main()
