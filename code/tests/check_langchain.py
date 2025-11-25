try:
    import langchain
    print(f"LangChain version: {langchain.__version__}")
    print(f"LangChain file: {langchain.__file__}")
except ImportError as e:
    print(f"Import failed: {e}")

try:
    from langfuse.callback import CallbackHandler
    print("Langfuse CallbackHandler import successful")
except ImportError as e:
    print(f"Langfuse CallbackHandler import failed: {e}")
except Exception as e:
    print(f"Langfuse CallbackHandler error: {e}")
