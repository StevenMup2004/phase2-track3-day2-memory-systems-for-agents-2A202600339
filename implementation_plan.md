# Implementation Plan - Lab #17: Build Multi-Memory Agent with LangGraph

Muc tieu: dat 100/100 theo rubric bang cach implement dung 5 nhom tieu chi va co bang chung kiem thu ro rang.

## 0) Deliverables bat buoc

Can nop day du cac file sau:
- Source code agent (LangGraph hoac skeleton LangGraph).
- Data files cho profile/episodes/semantic index.
- `BENCHMARK.md` co dung 10 multi-turn conversations, so sanh `no-memory` vs `with-memory`.
- `REFLECTION.md` ve privacy va limitations.

Neu thieu `BENCHMARK.md` hoac khong du 10 conversations thi khong the dat diem toi da.

## 1) Kien truc memory stack (25 diem)

Yeu cau full diem:
- Co du 4 memory types o muc interface (tach rieng, khong gop blob):
    - Short-term memory
    - Long-term profile memory
    - Episodic memory
    - Semantic memory
- Moi loai co ham `save`/`retrieve` rieng, ten ro y nghia.

De xuat cau truc:

```text
src/
    memory/
        short_term.py
        long_term.py
        episodic.py
        semantic.py
```

Hop dong interface toi thieu (goi y):
- `short_term.py`
    - `append_turn(user_id, role, content)`
    - `get_recent(user_id, k=10)`
- `long_term.py`
    - `upsert_fact(user_id, key, value, source=None, ts=None)`
    - `get_profile(user_id)`
- `episodic.py`
    - `save_episode(user_id, task, outcome, metadata=None)`
    - `get_recent_episodes(user_id, limit=5)`
- `semantic.py`
    - `index_documents(docs)`
    - `search(query, top_k=3)`

Backend mapping de hop rubric:
- Short-term: sliding window/list buffer.
- Long-term profile: JSON/KV store.
- Episodic: JSON list/log store.
- Semantic: Chroma/FAISS; neu khong co thi fallback keyword search (nhung van phai la module rieng).

## 2) LangGraph state/router + prompt injection (30 diem)

Yeu cau full diem:
- Co `MemoryState` (hoac state dict tuong duong) gom truong memory ro rang.
- Co node `retrieve_memory(state)` (ten co the khac, vai tro tuong duong).
- Router phai gom du lieu tu nhieu backends vao state.
- Prompt phai inject day du 4 section memory + recent conversation.
- Co trim/token budget co ban.

State de xuat:

```python
class MemoryState(TypedDict):
        messages: list
        user_profile: dict
        episodes: list[dict]
        semantic_hits: list[str]
        recent_conversation: list[dict]
        memory_budget: int
```

Flow toi thieu:
1. User message vao graph.
2. `retrieve_memory` lay profile + episodes + semantic hits + recent conversation.
3. `compose_prompt` inject thanh cac block rieng:
     - `[USER PROFILE]`
     - `[EPISODIC MEMORY]`
     - `[SEMANTIC HITS]`
     - `[RECENT CONVERSATION]`
4. Ap dung trim theo `memory_budget` truoc khi goi model.

Luu y quan trong: retrieve xong nhung khong dua vao prompt thi bi tru diem nang.

## 3) Save/update + conflict handling (15 diem)

Yeu cau full diem:
- Update duoc it nhat 2 profile facts.
- Co save episodic khi task hoan tat/co outcome ro.
- Fact moi ghi de fact cu khi mau thuan.
- Khong append vo toi va de profile xung dot.

Rule conflict de implement:
- Su dung key chuan hoa (vi du `allergy`, `name`, `timezone`).
- Moi key chi giu 1 gia tri hien hanh trong profile.
- Luu `history` de audit, nhung retrieval profile chinh chi tra ve gia tri moi nhat.

Test bat buoc (phai pass):
- Turn 1: "Toi di ung sua bo."
- Turn 2: "A nham, toi di ung dau nanh chu khong phai sua bo."
- Expected profile: `allergy = dau nanh`.

## 4) Benchmark 10 multi-turn conversations (20 diem)

Yeu cau full diem:
- `BENCHMARK.md` co dung 10 scenarios, moi scenario la multi-turn.
- Moi scenario co 2 cot so sanh: `no-memory` vs `with-memory`.
- Bao phu du 5 nhom test:
    - profile recall
    - conflict update
    - episodic recall
    - semantic retrieval
    - trim/token budget

Mau bang bat buoc trong `BENCHMARK.md`:

```text
| # | Scenario | No-memory result | With-memory result | Pass? |
```

Danh sach 10 scenarios de dam bao du coverage:
1. Nho ten user sau 6+ turns.
2. Nho timezone preference.
3. Cap nhat conflict allergy.
4. Cap nhat conflict city/hobby.
5. Recall task outcome da hoan tat (episodic).
6. Recall bugfix lesson truoc do (episodic).
7. Retrieve dung FAQ chunk 1 (semantic).
8. Retrieve dung FAQ chunk 2 (semantic).
9. Token budget trim khi context dai.
10. Ket hop profile + semantic trong cung mot tra loi.

Quy dinh dat:
- Moi scenario phai co transcript tom tat nhieu turn.
- Cot `Pass?` co tieu chi pass ro (khong danh gia cam tinh).

## 5) Reflection privacy/limitations (10 diem)

`REFLECTION.md` can tra loi truc dien cac cau hoi sau:
1. Ranh gioi PII nao dang duoc luu? Rui ro la gi?
2. Memory nao nhay cam nhat neu retrieve sai? Vi sao?
3. Neu user yeu cau xoa du lieu, can xoa o backend nao? Co TTL/consent khong?
4. 1-2 limitation ky thuat hien tai (vi du: quality retrieval, drift profile extraction, chi phi vector search, race condition khi ghi memory).

Checklist full diem:
- Co privacy risk cu the, khong viet chung chung.
- Co deletion flow (it nhat o muc procedure).
- Co noi ro failure mode khi scale.

## 6) Ke hoach thuc thi trong 2 gio

Phase 1 (0-30 phut):
- Tao 4 module memory + data schema.
- Tao bo du lieu semantic ban dau (FAQ/notes).

Phase 2 (30-70 phut):
- Tao `MemoryState`, `retrieve_memory`, `compose_prompt`, trim budget.
- Noi graph flow end-to-end, chay duoc 1 hoi thoai mau.

Phase 3 (70-100 phut):
- Implement save/update profile + episodic.
- Chay test conflict bat buoc va fix den khi pass.

Phase 4 (100-120 phut):
- Chay 10 benchmark conversations.
- Hoan thien `BENCHMARK.md` + `REFLECTION.md`.

## 7) Definition of Done (de tu check 100 diem)

- [ ] Co 4 memory types tach rieng, interface ro.
- [ ] Co state/router va node retrieve memory.
- [ ] Prompt co du 4 section memory + recent conversation.
- [ ] Co trim/token budget.
- [ ] Co save/update profile (>=2 facts) va conflict overwrite dung.
- [ ] Co save episodic theo outcome.
- [ ] `BENCHMARK.md` co dung 10 multi-turn, day du `no-memory` vs `with-memory`.
- [ ] Benchmark cover du 5 nhom test rubric.
- [ ] `REFLECTION.md` day du privacy + deletion/TTL/consent + limitations.

Neu tat ca checkbox deu dat, bai lam dat muc "Tot" o ca 5 hang muc va co kha nang dat 100/100.
