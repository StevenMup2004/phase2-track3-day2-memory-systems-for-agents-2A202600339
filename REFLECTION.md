# Reflection: Privacy and Limitations

## 1) PII and privacy risks

The system stores profile facts such as name, city, timezone, and allergy. These are personal data points.
If profile memory is leaked, an attacker can infer identity and sensitive preferences.

Potential privacy risks:
- Unauthorized access to profile.json and episodes.json.
- Over-retention of personal data without user consent.
- Prompt injection causing irrelevant sensitive memory to be surfaced.

## 2) Most sensitive memory type

Long-term profile memory is the most sensitive because it accumulates stable personal facts over time.
Episodic memory can also become sensitive if it contains operational details (incident names, internal systems).

## 3) Deletion, TTL, and consent strategy

Deletion flow on user request:
1. Delete user profile keys from data/profile.json.
2. Delete user episodes from data/episodes.json.
3. Remove semantic chunks if they contain user-specific sensitive content.
4. Clear short-term in-memory turns for the user session.

Retention and consent policy:
- Ask consent before storing profile facts beyond session scope.
- Apply TTL for episodic entries (for example 30 days).
- Keep a minimal audit trail with redacted values when possible.

## 4) Retrieval and safety limitations

Current limitations:
- Semantic retrieval uses keyword overlap fallback, which can miss relevant context or return false positives.
- Profile extraction is rule-based and may miss complex linguistic corrections.
- No robust access control is implemented in this lab setup.
- Token budgeting is approximate (word-based), not exact token counting.

Failure modes at scale:
- Larger semantic corpora can degrade retrieval quality without reranking.
- Concurrent writes to JSON stores can create race conditions.
- Memory contamination can occur across users if user_id handling is weak.

## 5) What helps most and what can fail most

Most helpful memory for user experience:
- Long-term profile + short-term context, because they improve personalization and continuity.

Highest risk if retrieval is wrong:
- Long-term profile retrieval, because incorrect personal facts can create trust and safety issues.
