"""Semantic memory backend for retrieval using ChromaDB."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import List

import chromadb
import requests
from chromadb import Documents, EmbeddingFunction, Embeddings

class RESTOpenAIEmbeddingFunction(EmbeddingFunction):
	def __init__(self, api_key: str, model_name: str = "text-embedding-3-small"):
		self.api_key = api_key
		self.model_name = model_name

	def __call__(self, input: Documents) -> Embeddings:
		if not self.api_key:
			return [[0.0] * 1536 for _ in input]
			
		response = requests.post(
			"https://api.openai.com/v1/embeddings",
			headers={
				"Authorization": f"Bearer {self.api_key}",
				"Content-Type": "application/json",
			},
			json={
				"input": input,
				"model": self.model_name
			},
			timeout=30
		)
		response.raise_for_status()
		data = response.json()
		# Return embeddings in the same order as the input
		return [item["embedding"] for item in sorted(data["data"], key=lambda x: x["index"])]


class SemanticMemory:
	"""Semantic retrieval using ChromaDB."""

	def __init__(self, docs_path: str | Path) -> None:
		self.docs_path = Path(docs_path)
		self.db_path = self.docs_path.parent / "chroma_db"
		
		# Create ChromaDB client
		self.client = chromadb.PersistentClient(path=str(self.db_path))
		
		api_key = os.getenv("OPENAI_API_KEY", "")
		openai_ef = RESTOpenAIEmbeddingFunction(
			api_key=api_key,
			model_name="text-embedding-3-small"
		)
		
		# Use a new collection name to avoid dimension mismatch with previous default embeddings
		self.collection = self.client.get_or_create_collection(
			name="semantic_docs_v3",
			embedding_function=openai_ef
		)
		
		# Optional: Keep JSON just for seed tracking
		self.docs_path.parent.mkdir(parents=True, exist_ok=True)
		if not self.docs_path.exists():
			self.docs_path.write_text("[]", encoding="utf-8")

	def index_documents(self, docs: List[dict]) -> None:
		"""Index documents into ChromaDB."""
		ids = []
		documents = []
		metadatas = []
		
		for i, doc in enumerate(docs):
			doc_id = doc.get("id", f"doc-{i}")
			ids.append(doc_id)
			documents.append(doc.get("text", ""))
			metadatas.append({"tags": ",".join(doc.get("tags", []))})
			
		if ids:
			self.collection.upsert(
				ids=ids,
				documents=documents,
				metadatas=metadatas
			)
			
		# Update JSON for backup/reference
		self.docs_path.write_text(
			json.dumps(docs, ensure_ascii=False, indent=2), encoding="utf-8"
		)

	def search(self, query: str, top_k: int = 3) -> List[str]:
		"""Search documents using ChromaDB."""
		if top_k <= 0 or not query.strip():
			return []
			
		results = self.collection.query(
			query_texts=[query],
			n_results=min(top_k, self.collection.count() or 1)
		)
		
		if results and results.get("documents") and results["documents"][0]:
			return results["documents"][0]
		return []

