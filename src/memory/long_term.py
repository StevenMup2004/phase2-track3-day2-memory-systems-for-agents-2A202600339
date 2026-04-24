"""Long-term profile memory backend with conflict handling."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional


def _utc_now() -> str:
	return datetime.now(timezone.utc).isoformat()


class LongTermProfileMemory:
	"""JSON-backed profile store with overwrite-on-conflict semantics."""

	def __init__(self, profile_path: str | Path) -> None:
		self.profile_path = Path(profile_path)
		self.profile_path.parent.mkdir(parents=True, exist_ok=True)
		if not self.profile_path.exists():
			self.profile_path.write_text("{}", encoding="utf-8")

	def _load(self) -> dict:
		try:
			return json.loads(self.profile_path.read_text(encoding="utf-8"))
		except json.JSONDecodeError:
			return {}

	def _save(self, payload: dict) -> None:
		self.profile_path.write_text(
			json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
		)

	def get_profile(self, user_id: str) -> Dict[str, str]:
		payload = self._load()
		return payload.get(user_id, {}).get("profile", {})

	def upsert_fact(
		self,
		user_id: str,
		key: str,
		value: str,
		source: Optional[str] = None,
		ts: Optional[str] = None,
	) -> None:
		payload = self._load()
		user_slot = payload.setdefault(user_id, {"profile": {}, "history": []})
		profile: dict = user_slot.setdefault("profile", {})
		history: list = user_slot.setdefault("history", [])

		old_value = profile.get(key)
		profile[key] = value
		history.append(
			{
				"key": key,
				"old_value": old_value,
				"new_value": value,
				"source": source or "user_message",
				"timestamp": ts or _utc_now(),
			}
		)
		self._save(payload)

	def update_from_text(self, user_id: str, text: str, client=None, model: str = "gpt-4o-mini") -> Dict[str, str]:
		"""Extract profile facts from user text using LLM and upsert with conflict override."""
		if not client:
			return {}
			
		facts = extract_profile_facts_llm(text, client, model)
		for key, value in facts.items():
			self.upsert_fact(user_id=user_id, key=key, value=value, source="llm_extractor")
		return facts


def extract_profile_facts_llm(text: str, client, model: str) -> Dict[str, str]:
	"""LLM-based profile extractor."""
	system_prompt = (
		"You are a profile extraction system. Your task is to extract user facts from the following text.\n"
		"Supported keys: name, timezone, city, hobby, allergy.\n"
		"IMPORTANT RULES:\n"
		"1. Only extract facts stated by the user. Do NOT extract question words.\n"
		"   If the user asks 'Tôi tên là gì?' (What is my name?), do NOT extract 'gì' as the name. Return nothing.\n"
		"2. If the user corrects a previous fact (e.g., 'no wait, I am allergic to soy, not milk'), extract ONLY the new corrected fact ('đậu nành').\n"
		"3. Output a pure JSON object. Omit keys that are not present. Example: {\"name\": \"Alice\", \"allergy\": \"đậu nành\"}\n"
		"4. Translate attributes to short descriptive values (e.g., 'đậu nành' instead of 'dị ứng đậu nành').\n"
	)
	
	try:
		import os
		import requests
		api_key = os.getenv("OPENAI_API_KEY", "")
		if not api_key:
			return {}

		response = requests.post(
			"https://api.openai.com/v1/chat/completions",
			headers={
				"Authorization": f"Bearer {api_key}",
				"Content-Type": "application/json",
			},
			json={
				"model": model,
				"temperature": 0,
				"response_format": {"type": "json_object"},
				"messages": [
					{"role": "system", "content": system_prompt},
					{"role": "user", "content": text},
				]
			},
			timeout=30
		)
		response.raise_for_status()
		data = response.json()
		content = data["choices"][0]["message"]["content"]
		if not content:
			return {}
		return json.loads(content)
	except Exception as e:
		print(f"Error during LLM extraction: {e}")
		return {}
