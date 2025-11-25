
"""
LangChain Compatibility Patch
=============================

This module patches the runtime environment to make older libraries (like gpt-researcher)
compatible with newer versions of LangChain (>= 0.3).

It mocks removed modules and redirects imports to their new locations.
Must be imported BEFORE any other langchain or gpt-researcher imports.
"""

import sys
import types
import warnings
import logging

logger = logging.getLogger("patch_langchain")

def apply_patches():
    """Apply all langchain compatibility patches."""
    
    # Suppress Pydantic V2 warnings from langchain
    # Suppress Pydantic V2 warnings from langchain - ONLY specific ones if needed
    # warnings.filterwarnings("ignore", category=UserWarning, module="langchain")
    
    # 1. Patch langchain.docstore
    if "langchain.docstore" not in sys.modules:
        try:
            from langchain_core.documents import Document
            docstore = types.ModuleType("langchain.docstore")
            document = types.ModuleType("langchain.docstore.document")
            document.Document = Document
            docstore.document = document
            sys.modules["langchain.docstore"] = docstore
            sys.modules["langchain.docstore.document"] = document
            # logger.info("Patched langchain.docstore")
        except ImportError:
            pass

    # 2. Patch langchain.vectorstores
    if "langchain.vectorstores" not in sys.modules:
        try:
            from langchain_core.vectorstores import VectorStore
            vectorstores = types.ModuleType("langchain.vectorstores")
            vectorstores.VectorStore = VectorStore
            sys.modules["langchain.vectorstores"] = vectorstores
            # logger.info("Patched langchain.vectorstores")
        except ImportError:
            pass

    # 3. Patch langchain.text_splitter
    if "langchain.text_splitter" not in sys.modules:
        try:
            from langchain_text_splitters import RecursiveCharacterTextSplitter
            text_splitter = types.ModuleType("langchain.text_splitter")
            text_splitter.RecursiveCharacterTextSplitter = RecursiveCharacterTextSplitter
            sys.modules["langchain.text_splitter"] = text_splitter
            # logger.info("Patched langchain.text_splitter")
        except ImportError:
            pass

    # 4. Patch langchain.callbacks
    if "langchain.callbacks" not in sys.modules:
        try:
            from langchain_core.callbacks import manager
            callbacks = types.ModuleType("langchain.callbacks")
            callbacks.manager = manager
            sys.modules["langchain.callbacks"] = callbacks
            sys.modules["langchain.callbacks.manager"] = manager
            # logger.info("Patched langchain.callbacks")
        except ImportError:
            pass

    # 5. Patch langchain.schema
    if "langchain.schema" not in sys.modules:
        try:
            from langchain_core import documents
            from langchain_core import retrievers
            schema = types.ModuleType("langchain.schema")
            schema.__path__ = [] 
            schema.Document = documents.Document
            sys.modules["langchain.schema"] = schema
            
            schema_retriever = types.ModuleType("langchain.schema.retriever")
            schema_retriever.BaseRetriever = retrievers.BaseRetriever
            sys.modules["langchain.schema.retriever"] = schema_retriever
            # logger.info("Patched langchain.schema")
        except ImportError:
            pass

    # 6. Patch langchain.retrievers (CRITICAL FIX)
    # This is the most persistent error. We need to be aggressive.
    try:
        # Ensure langchain package is loaded
        import langchain
        
        # Create retrievers module if it doesn't exist or is empty
        if "langchain.retrievers" not in sys.modules:
            retrievers_module = types.ModuleType("langchain.retrievers")
            retrievers_module.__path__ = []
            sys.modules["langchain.retrievers"] = retrievers_module
        else:
            retrievers_module = sys.modules["langchain.retrievers"]
        
        # Import necessary classes from new locations
        # ContextualCompressionRetriever moved to langchain.retrievers.contextual_compression
        # But in 0.3 it might be in langchain.retrievers directly or langchain_community
        
        # Try to find the class
        ContextualCompressionRetriever = None
        try:
            from langchain.retrievers import ContextualCompressionRetriever
        except ImportError:
            try:
                from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
            except ImportError:
                pass
        
        if ContextualCompressionRetriever:
             retrievers_module.ContextualCompressionRetriever = ContextualCompressionRetriever
        else:
            # Mock it if we can't find it, to prevent import error
            class MockContextualCompressionRetriever:
                pass
            retrievers_module.ContextualCompressionRetriever = MockContextualCompressionRetriever

        # Also patch document_compressors
        document_compressors = types.ModuleType("langchain.retrievers.document_compressors")
        
        # Try to find DocumentCompressorPipeline
        DocumentCompressorPipeline = None
        try:
            from langchain.retrievers.document_compressors import DocumentCompressorPipeline
        except ImportError:
            try:
                from langchain_community.retrievers.document_compressors import DocumentCompressorPipeline
            except ImportError:
                pass
                
        if DocumentCompressorPipeline:
            document_compressors.DocumentCompressorPipeline = DocumentCompressorPipeline
        else:
            class MockDocumentCompressorPipeline:
                pass
            document_compressors.DocumentCompressorPipeline = MockDocumentCompressorPipeline

        # Try to find EmbeddingsFilter
        EmbeddingsFilter = None
        try:
            from langchain.retrievers.document_compressors import EmbeddingsFilter
        except ImportError:
            try:
                from langchain_community.retrievers.document_compressors import EmbeddingsFilter
            except ImportError:
                pass

        if EmbeddingsFilter:
            document_compressors.EmbeddingsFilter = EmbeddingsFilter
        else:
            class MockEmbeddingsFilter:
                def __init__(self, embeddings=None, similarity_threshold=0.76, k=20):
                    pass
            document_compressors.EmbeddingsFilter = MockEmbeddingsFilter

        # Try to find LLMChainExtractor
        LLMChainExtractor = None
        try:
            from langchain.retrievers.document_compressors import LLMChainExtractor
        except ImportError:
            try:
                from langchain_community.retrievers.document_compressors import LLMChainExtractor
            except ImportError:
                pass

        if LLMChainExtractor:
            document_compressors.LLMChainExtractor = LLMChainExtractor
        else:
            class MockLLMChainExtractor:
                @classmethod
                def from_llm(cls, llm):
                    return cls()
            document_compressors.LLMChainExtractor = MockLLMChainExtractor

        # Try to find LLMChainFilter
        LLMChainFilter = None
        try:
            from langchain.retrievers.document_compressors import LLMChainFilter
        except ImportError:
            try:
                from langchain_community.retrievers.document_compressors import LLMChainFilter
            except ImportError:
                pass

        if LLMChainFilter:
            document_compressors.LLMChainFilter = LLMChainFilter
        else:
            class MockLLMChainFilter:
                @classmethod
                def from_llm(cls, llm):
                    return cls()
            document_compressors.LLMChainFilter = MockLLMChainFilter
            
        sys.modules["langchain.retrievers.document_compressors"] = document_compressors
        
        # Inject into langchain package
        langchain.retrievers = retrievers_module
        
        # logger.info("Patched langchain.retrievers")
        
    except ImportError as e:
        # Fallback if imports fail
        pass
    except Exception as e:
        logger.warning(f"Failed to patch langchain.retrievers: {e}")

    # 7. Patch langchain.output_parsers
    if "langchain.output_parsers" not in sys.modules:
        try:
            from langchain_core import output_parsers as core_parsers
            output_parsers = types.ModuleType("langchain.output_parsers")
            output_parsers.PydanticOutputParser = core_parsers.PydanticOutputParser
            sys.modules["langchain.output_parsers"] = output_parsers
            # logger.info("Patched langchain.output_parsers")
        except ImportError:
             # Create mock if import fails
            output_parsers = types.ModuleType("langchain.output_parsers")
            class MockPydanticOutputParser:
                pass
            output_parsers.PydanticOutputParser = MockPydanticOutputParser
            sys.modules["langchain.output_parsers"] = output_parsers

    # 8. Patch langchain.prompts
    if "langchain.prompts" not in sys.modules:
        try:
            from langchain_core import prompts as core_prompts
            prompts = types.ModuleType("langchain.prompts")
            prompts.PromptTemplate = core_prompts.PromptTemplate
            prompts.ChatPromptTemplate = core_prompts.ChatPromptTemplate
            sys.modules["langchain.prompts"] = prompts
            # logger.info("Patched langchain.prompts")
        except ImportError:
            # Create mock if import fails
            prompts = types.ModuleType("langchain.prompts")
            class MockPromptTemplate:
                pass
            class MockChatPromptTemplate:
                pass
            prompts.PromptTemplate = MockPromptTemplate
            prompts.ChatPromptTemplate = MockChatPromptTemplate
            sys.modules["langchain.prompts"] = prompts

# Apply patches immediately on import
apply_patches()
