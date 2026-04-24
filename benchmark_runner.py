"""Run 10 multi-turn benchmark scenarios and collect results."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from src.agent import MemoryAgent


@dataclass
class Scenario:
	idx: int
	title: str
	turns: list[str]
	expected_contains: tuple[str, ...]


def _run_conversation(agent: MemoryAgent, user_id: str, turns: list[str]) -> str:
	final_reply = ""
	for msg in turns:
		final_reply = agent.chat(user_id=user_id, user_message=msg, memory_budget=220)
	return final_reply


def _judge_pass(reply: str, expected_contains: tuple[str, ...]) -> bool:
	return any(ex.lower() in reply.lower() for ex in expected_contains)


def _build_scenarios() -> List[Scenario]:
	return [
		Scenario(
			1,
			"Profile recall: remember user name after delay",
			[
				"Tôi tên là Vũ Hải Đăng.",
				"Hãy nêu 3 mẹo debug Python.",
				"Cảm ơn.",
				"Tôi tên là gì?",
			],
			("vũ hải đăng",),
		),
		Scenario(
			2,
			"Profile recall: remember timezone preference",
			[
				"Tôi ở múi giờ Asia/Ho_Chi_Minh.",
				"Cho tôi checklist deploy nhanh.",
				"Timezone của tôi là gì?",
			],
			("asia/ho_chi_minh",),
		),
		Scenario(
			3,
			"Conflict update: allergy corrected",
			[
				"Tôi dị ứng sữa bò.",
				"À nhầm, tôi dị ứng đậu nành chứ không phải sữa bò.",
				"Tôi dị ứng gì?",
			],
			("đậu nành",),
		),
		Scenario(
			4,
			"Conflict update: city overwritten",
			[
				"Tôi sống ở Đà Nẵng.",
				"Xin sửa, hiện tại tôi sống ở Hà Nội.",
				"Tôi đang sống ở đâu?",
			],
			("hà nội",),
		),
		Scenario(
			5,
			"Episodic recall: completed task outcome",
			[
				"Đã fixed xong bug timeout cho API gateway.",
				"Tôi vừa hoàn tất việc gì?",
			],
			("timeout",),
		),
		Scenario(
			6,
			"Episodic recall: resolved issue tracking",
			[
				"Issue import report đã resolved và xong.",
				"Tôi vừa giải quyết issue nào?",
			],
			("issue", "vấn đề", "import report", "báo cáo nhập"),
		),
		Scenario(
			7,
			"Semantic retrieval: Windows encoding fix",
			[
				"Theo tài liệu nội bộ, làm sao để tránh lỗi cp1252 decode crash khi đọc file source trên Windows? Trả lời 1 câu ngắn gọn.",
			],
			("utf-8", "errors='ignore'", "errors=ignore", "utf8", "ignore"),
		),
		Scenario(
			8,
			"Semantic retrieval: FastAPI header deletion",
			[
				"Theo tài liệu nội bộ, xóa header trong FastAPI middleware sử dụng object nào (request hay response)? Trả lời đúng 1 dòng ngắn gọn kèm theo câu lệnh đó.",
			],
			("del response.headers", "response.headers", "đối tượng response", "biến response", "response"),
		),
		Scenario(
			9,
			"Token budget trim under long context",
			[
				"Tôi tên là Vũ Hải Đăng.",
				"".join(["spam "] * 180),
				"Chỉ trả lời ngắn gọn tên tôi là gì (tối đa 5 từ).",
			],
			("vũ hải đăng",),
		),
		Scenario(
			10,
			"Combined profile + semantic in one response",
			[
				"Tôi tên là Vũ Hải Đăng.",
				"Theo tài liệu nội bộ, làm sao để check git cho repo-scoped khi workspace có nhiều extension diffs? Gọi tên tôi và trả lời bằng 1 câu lệnh git ngắn gọn.",
			],
			("-c", "<repo>", "status", "hải đăng"),
		),
	]


def run_benchmark(project_root: Path, use_openai: bool = True) -> str:
	scenarios = _build_scenarios()
	with_memory = MemoryAgent(project_root=project_root, enable_memory=True, use_openai=use_openai)
	no_memory = MemoryAgent(project_root=project_root, enable_memory=False, use_openai=use_openai)

	rows: list[str] = []
	pass_count = 0

	for sc in scenarios:
		no_reply = _run_conversation(no_memory, user_id=f"nm_{sc.idx}", turns=sc.turns)
		with_reply = _run_conversation(with_memory, user_id=f"wm_{sc.idx}", turns=sc.turns)
		passed = _judge_pass(with_reply, sc.expected_contains)
		pass_count += int(passed)

		rows.append(
			"| {idx} | {title} | {nm} | {wm} | {passed} |".format(
				idx=sc.idx,
				title=sc.title,
				nm=no_reply.replace("|", "\\|").replace("\n", "<br>"),
				wm=with_reply.replace("|", "\\|").replace("\n", "<br>"),
				passed="Pass" if passed else "Fail",
			)
		)

	content = "\n".join(
		[
			"# BENCHMARK",
			"",
			"Comparison of no-memory vs with-memory across 10 multi-turn conversations.",
			"",
			"| # | Scenario | No-memory result | With-memory result | Pass? |",
			"|---|----------|------------------|--------------------|-------|",
			*rows,
			"",
			f"Overall pass rate (with-memory expectation): {pass_count}/10",
			"",
			"Notes:",
			"- No-memory baseline disables memory retrieval and persistence.",
			"- With-memory mode enables profile, episodic, semantic, and short-term retrieval.",
		]
	)
	out_path = project_root / "BENCHMARK.md"
	out_path.write_text(content, encoding="utf-8")
	return content


if __name__ == "__main__":
	root = Path(__file__).resolve().parent
	run_benchmark(project_root=root, use_openai=True)
	print("BENCHMARK.md generated.")

