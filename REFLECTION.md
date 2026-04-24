# Reflection: Privacy, Real API Usage, and Limitations

## 0) Current implementation snapshot (updated)

This lab is currently running with real API calls, not mock-only logic:
- Assistant generation calls OpenAI Chat Completions via HTTPS.
- Long-term profile extraction also calls OpenAI Chat Completions with JSON output mode.
- Semantic memory uses ChromaDB (persistent local vector store) and OpenAI Embeddings API.

Benchmark status is 10/10 with no-memory vs with-memory comparison on 10 multi-turn conversations.
The realistic policy scenarios (QD-17, HT-22, BM-47) show that no-memory can answer with plausible but wrong values, while with-memory returns the expected stored policy facts.

## 1) PII and privacy risks

Stored personal information includes profile facts such as name, city, timezone, hobby, and allergy.
Episodic memory can store operational details (for example complaint IDs and completed tasks).

Main privacy risks:
- Unauthorized local access to data/profile.json, data/episodes.json, and Chroma persistence under data/chroma_db.
- Data transfer to third-party API providers (OpenAI) if prompts contain personal or sensitive content.
- Over-retention without explicit retention windows.
- Prompt injection or broad retrieval that surfaces sensitive memory out of scope.

## 2) Most sensitive memory type

Most sensitive: long-term profile memory.
Reason: it accumulates stable personal identity attributes and can be abused for profiling if leaked.

Second most sensitive: episodic memory.
Reason: it can expose historical events, issue IDs, and workflow outcomes.

Semantic memory is sensitive mainly when internal policy text or user-specific notes are indexed.

## 3) Deletion, TTL, and consent strategy

Deletion flow on user request (current backend mapping):
1. Remove user profile entry by user_id from data/profile.json.
2. Remove user episodes by user_id from data/episodes.json.
3. Delete user-specific semantic docs from data/semantic_docs.json and corresponding vectors in Chroma collection.
4. Clear short-term in-memory turns for that user session.

Retention and consent policy:
- Ask consent before persisting profile facts beyond one session.
- Suggested TTL: episodic entries 30 days, profile facts 90 days unless user opts in for longer retention.
- Provide an opt-out mode that keeps only short-term session memory.

## 4) Technical limitations and safety gaps

Current limitations in this implementation:
- It depends on external OpenAI availability, network stability, and quota.
- No PII redaction layer before sending content to external APIs.
- No authentication/authorization layer for local data access in this lab setup.
- Local JSON writes are not transactional and can race under concurrent writers.
- Token budgeting is approximate (word-count based), not tokenizer-accurate.
- Profile extraction is LLM-based and can still fail on ambiguous or mixed-language corrections.

## 5) Failure modes at scale and priorities

Likely failure modes at scale:
- Higher latency/cost due to repeated API calls (generation, extraction, embeddings).
- Retrieval quality drift as semantic corpus grows without reranking or filtering.
- Cross-user contamination risk if user_id hygiene is not strictly enforced.

Hardening priorities:
1. Add PII masking/redaction before external API calls.
2. Add delete APIs per backend plus periodic TTL cleanup jobs.
3. Add lock/transaction strategy for file-based writes (or migrate profile/episodes to DB/Redis).
4. Add retrieval guardrails (scope filters + confidence checks) before injecting memory.

## 6) What helps most vs what can fail most

Most helpful memory for user experience:
- Long-term profile + short-term context for personalization and continuity.

Highest-risk failure if wrong retrieval occurs:
- Long-term profile retrieval, because wrong personal facts directly damage trust and can create privacy/safety issues.
