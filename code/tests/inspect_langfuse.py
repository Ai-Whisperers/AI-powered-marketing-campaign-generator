import langfuse

print(f"Langfuse version: {langfuse.version.__version__}")
print(f"Dir langfuse: {dir(langfuse)}")
try:
    from langfuse.callback import CallbackHandler
    print("Import successful")
except ImportError as e:
    print(f"Import failed: {e}")
