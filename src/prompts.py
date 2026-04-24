"""Prompt templates with explicit memory sections."""

from __future__ import annotations

import json
from typing import List


BASE_INSTRUCTION = (
	"You are a helpful memory-enabled assistant. Use provided memory sections first. "
	"If memory conflicts, prioritize the most recent profile facts. "
	"Be concise and factual."
)


def _trim_lines(lines: list[str], budget: int) -> list[str]:
	"""Approximate trim by word budget."""
	if budget <= 0:
		return []
	out: list[str] = []
	used = 0
	for line in lines:
		cost = max(1, len(line.split()))
		if used + cost > budget:
			break
		out.append(line)
		used += cost
	return out


def build_system_prompt(
	user_profile: dict,
	episodes: list[dict],
	semantic_hits: List[str],
	recent_conversation: list[dict],
	memory_budget: int,
) -> str:
	profile_block = json.dumps(user_profile, ensure_ascii=False)
	episode_lines = [f"- task={ep.get('task')} | outcome={ep.get('outcome')}" for ep in episodes]
	semantic_lines = [f"- {hit}" for hit in semantic_hits]
	convo_lines = [f"- {msg.get('role')}: {msg.get('content')}" for msg in recent_conversation]

	episode_lines = _trim_lines(episode_lines, max(1, memory_budget // 4))
	semantic_lines = _trim_lines(semantic_lines, max(1, memory_budget // 4))
	convo_lines = _trim_lines(convo_lines, max(1, memory_budget // 2))

	return "\n".join(
		[
			BASE_INSTRUCTION,
			"",
			"[USER PROFILE]",
			profile_block,
			"",
			"[EPISODIC MEMORY]",
			"\n".join(episode_lines) if episode_lines else "- none",
			"",
			"[SEMANTIC HITS]",
			"\n".join(semantic_lines) if semantic_lines else "- none",
			"",
			"[RECENT CONVERSATION]",
			"\n".join(convo_lines) if convo_lines else "- none",
		]
	)

