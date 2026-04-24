"""LangGraph agent definition (state, router, nodes)."""

from __future__ import annotations

import os
import unicodedata
from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph

from src.memory.episodic import EpisodicMemory
from src.memory.long_term import LongTermProfileMemory
from src.memory.semantic import SemanticMemory
from src.memory.short_term import ShortTermMemory
from src.prompts import build_system_prompt

try:
	from openai import OpenAI
except ImportError:  # pragma: no cover
	OpenAI = None


class MemoryState(TypedDict, total=False):
	user_id: str
	user_message: str
	messages: list
	user_profile: dict
	episodes: list[dict]
	semantic_hits: list[str]
	recent_conversation: list[dict]
	memory_budget: int
	system_prompt: str
	assistant_reply: str


class MemoryAgent:
	def __init__(
		self,
		project_root: str | Path,
		enable_memory: bool = True,
		use_openai: bool = True,
		model: str = "gpt-4o-mini",
	) -> None:
		self.project_root = Path(project_root)
		load_dotenv(self.project_root / ".env")

		self.enable_memory = enable_memory
		self.use_openai = use_openai
		self.model = model

		self.short_term = ShortTermMemory(window_size=10)
		self.long_term = LongTermProfileMemory(self.project_root / "data" / "profile.json")
		self.episodic = EpisodicMemory(self.project_root / "data" / "episodes.json")
		self.semantic = SemanticMemory(self.project_root / "data" / "semantic_docs.json")

		self._ensure_seed_semantic_docs()
		self.client = self._build_openai_client()
		self.graph = self._build_graph()

	def _ensure_seed_semantic_docs(self) -> None:
		docs_file = self.project_root / "data" / "semantic_docs.json"
		if docs_file.exists() and docs_file.stat().st_size > 10:
			return
		seed_docs = [
			{
				"id": "faq-docker-service-name",
				"text": "In Docker Compose, backend should call peer service by service name, not localhost.",
				"tags": ["docker", "networking"],
			},
			{
				"id": "faq-header-delete",
				"text": "In FastAPI middleware, remove header via del response.headers['header-name'].",
				"tags": ["fastapi", "middleware"],
			},
			{
				"id": "faq-encoding",
				"text": "On Windows, read source files with UTF-8 and errors='ignore' to avoid cp1252 decode crash.",
				"tags": ["windows", "encoding"],
			},
			{
				"id": "faq-git-scope",
				"text": "Use git -C <repo> status and diff for repo-scoped checks when workspace has irrelevant extension diffs.",
				"tags": ["git", "workflow"],
			},
		]
		self.semantic.index_documents(seed_docs)

	def _build_openai_client(self):
		api_key = os.getenv("OPENAI_API_KEY", "")
		if not self.use_openai or not api_key or OpenAI is None:
			return None
		return OpenAI(api_key=api_key)

	def _build_graph(self):
		graph = StateGraph(MemoryState)
		graph.add_node("retrieve_memory", self.retrieve_memory)
		graph.add_node("compose_prompt", self.compose_prompt)
		graph.add_node("generate", self.generate)
		graph.add_node("persist_memory", self.persist_memory)

		graph.add_edge(START, "retrieve_memory")
		graph.add_edge("retrieve_memory", "compose_prompt")
		graph.add_edge("compose_prompt", "generate")
		graph.add_edge("generate", "persist_memory")
		graph.add_edge("persist_memory", END)
		return graph.compile()

	def retrieve_memory(self, state: MemoryState) -> MemoryState:
		user_id = state["user_id"]
		budget = int(state.get("memory_budget", 220))

		if not self.enable_memory:
			return {
				**state,
				"user_profile": {},
				"episodes": [],
				"semantic_hits": [],
				"recent_conversation": [],
				"memory_budget": budget,
			}

		return {
			**state,
			"user_profile": self.long_term.get_profile(user_id),
			"episodes": self.episodic.get_recent_episodes(user_id, limit=5),
			"semantic_hits": self.semantic.search(state["user_message"], top_k=3),
			"recent_conversation": self.short_term.get_recent(user_id, k=10),
			"memory_budget": budget,
		}

	def compose_prompt(self, state: MemoryState) -> MemoryState:
		prompt = build_system_prompt(
			user_profile=state.get("user_profile", {}),
			episodes=state.get("episodes", []),
			semantic_hits=state.get("semantic_hits", []),
			recent_conversation=state.get("recent_conversation", []),
			memory_budget=int(state.get("memory_budget", 220)),
		)
		return {**state, "system_prompt": prompt}

	def _llm_reply(self, system_prompt: str, user_message: str) -> str:
		api_key = os.getenv("OPENAI_API_KEY", "")
		if not api_key:
			return "Error: OPENAI_API_KEY is not configured properly in .env."

		try:
			import requests
			response = requests.post(
				"https://api.openai.com/v1/chat/completions",
				headers={
					"Authorization": f"Bearer {api_key}",
					"Content-Type": "application/json",
				},
				json={
					"model": self.model,
					"temperature": 0,
					"messages": [
						{"role": "system", "content": system_prompt},
						{"role": "user", "content": user_message},
					]
				},
				timeout=30
			)
			response.raise_for_status()
			data = response.json()
			return (data["choices"][0]["message"]["content"] or "").strip()
		except Exception as e:
			return f"Error from OpenAI API: {str(e)}"

	def generate(self, state: MemoryState) -> MemoryState:
		reply = self._llm_reply(
			system_prompt=state.get("system_prompt", ""),
			user_message=state["user_message"],
		)
		return {**state, "assistant_reply": reply}

	def persist_memory(self, state: MemoryState) -> MemoryState:
		user_id = state["user_id"]
		user_message = state["user_message"]
		assistant_reply = state.get("assistant_reply", "")

		if self.enable_memory:
			self.short_term.append_turn(user_id, "user", user_message)
			self.short_term.append_turn(user_id, "assistant", assistant_reply)

			self.long_term.update_from_text(
				user_id, user_message, client="REST", model=self.model
			)

			low = user_message.lower()
			if any(k in low for k in ["done", "hoan tat", "xong", "resolved", "fixed"]):
				self.episodic.save_episode(
					user_id=user_id,
					task="user_reported_task",
					outcome=user_message,
					metadata={"assistant_reply": assistant_reply[:180]},
				)

		return state

	def chat(self, user_id: str, user_message: str, memory_budget: int = 220) -> str:
		state: MemoryState = {
			"user_id": user_id,
			"user_message": user_message,
			"memory_budget": memory_budget,
			"messages": [],
		}
		out = self.graph.invoke(state)
		return out.get("assistant_reply", "")

