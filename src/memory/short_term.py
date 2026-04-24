"""Short-term memory backend (sliding window)."""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List


class ShortTermMemory:
	"""In-memory sliding window for recent turns by user."""

	def __init__(self, window_size: int = 10) -> None:
		self.window_size = max(1, window_size)
		self._store: Dict[str, List[dict]] = defaultdict(list)

	def append_turn(self, user_id: str, role: str, content: str) -> None:
		turns = self._store[user_id]
		turns.append({"role": role, "content": content})
		if len(turns) > self.window_size:
			self._store[user_id] = turns[-self.window_size :]

	def get_recent(self, user_id: str, k: int = 10) -> List[dict]:
		turns = self._store.get(user_id, [])
		if k <= 0:
			return []
		return turns[-k:]

	def clear(self, user_id: str) -> None:
		self._store.pop(user_id, None)

	def clear_all(self) -> None:
		self._store.clear()

