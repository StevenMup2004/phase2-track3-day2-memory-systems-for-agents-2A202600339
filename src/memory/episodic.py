"""Episodic memory backend for outcome logging."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional


def _utc_now() -> str:
	return datetime.now(timezone.utc).isoformat()


class EpisodicMemory:
	"""Append-only episode log in JSON format."""

	def __init__(self, episodes_path: str | Path) -> None:
		self.episodes_path = Path(episodes_path)
		self.episodes_path.parent.mkdir(parents=True, exist_ok=True)
		if not self.episodes_path.exists():
			self.episodes_path.write_text("[]", encoding="utf-8")

	def _load(self) -> list:
		try:
			return json.loads(self.episodes_path.read_text(encoding="utf-8"))
		except json.JSONDecodeError:
			return []

	def _save(self, episodes: list) -> None:
		self.episodes_path.write_text(
			json.dumps(episodes, ensure_ascii=False, indent=2), encoding="utf-8"
		)

	def save_episode(
		self,
		user_id: str,
		task: str,
		outcome: str,
		metadata: Optional[dict] = None,
	) -> None:
		episodes = self._load()
		episodes.append(
			{
				"user_id": user_id,
				"task": task,
				"outcome": outcome,
				"metadata": metadata or {},
				"timestamp": _utc_now(),
			}
		)
		self._save(episodes)

	def get_recent_episodes(self, user_id: str, limit: int = 5) -> List[dict]:
		episodes = [ep for ep in self._load() if ep.get("user_id") == user_id]
		if limit <= 0:
			return []
		return episodes[-limit:]

