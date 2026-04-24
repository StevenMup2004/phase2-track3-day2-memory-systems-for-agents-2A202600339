import os
import chromadb.utils.embedding_functions as embedding_functions

try:
    ef = embedding_functions.OpenAIEmbeddingFunction(api_key="sk-fake", model_name="text-embedding-3-small")
    ef(["test"])
    print("SUCCESS")
except Exception as e:
    print(f"FAILED: {e}")
