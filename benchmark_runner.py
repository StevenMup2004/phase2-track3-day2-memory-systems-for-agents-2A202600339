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
	low = reply.lower()
	return all(ex.lower() in low for ex in expected_contains)


def _build_benchmark_semantic_docs() -> list[dict]:
	"""Semantic corpus used in benchmark to test retrieval on realistic policies."""
	return [
		{
			"id": "policy-qd17",
			"text": "Theo quy chế nội bộ QD-17, khiếu nại cấp 1 phải được phản hồi trong 36 giờ.",
			"tags": ["quy-che", "khieu-nai"],
		},
		{
			"id": "policy-ht22",
			"text": "Theo quy trình HT-22, hồ sơ KYC nhóm B phải lưu tối thiểu 18 tháng.",
			"tags": ["kyc", "lưu-trữ"],
		},
		{
			"id": "policy-bm47",
			"text": "Theo hướng dẫn BM-47, giao dịch treo cần hoàn tiền trong 5 ngày làm việc.",
			"tags": ["hoan-tien", "ngan-hang"],
		},
		{
			"id": "policy-pl09",
			"text": "Theo điều khoản PL-09, hợp đồng thử việc cần báo trước 3 ngày.",
			"tags": ["hop-dong", "lao-dong"],
		},
	]


def _build_scenarios() -> List[Scenario]:
	return [
		Scenario(
			1,
			"Profile recall: remember user name after daily planning",
			[
				"Mình tên là Vũ Hải Đăng.",
				"Tuần này mình đang chuẩn bị hồ sơ vay mua xe.",
				"Nhắc lại tên mình là gì?",
			],
			("vũ hải đăng",),
		),
		Scenario(
			2,
			"Profile recall: remember timezone preference",
			[
				"Mình đang sống ở múi giờ Asia/Ho_Chi_Minh.",
				"Lịch uống thuốc của mình là 7h sáng hằng ngày.",
				"Múi giờ mình dùng là gì?",
			],
			("asia/ho_chi_minh",),
		),
		Scenario(
			3,
			"Conflict update: allergy corrected",
			[
				"Mình dị ứng đậu phộng.",
				"Đính chính: mình dị ứng hải sản, không phải đậu phộng.",
				"Mình dị ứng gì?",
			],
			("hải sản",),
		),
		Scenario(
			4,
			"Conflict update: city overwritten",
			[
				"Hiện tại mình sống ở Đà Nẵng.",
				"Cập nhật giúp: giờ mình chuyển ra Hà Nội.",
				"Mình đang sống ở đâu?",
			],
			("hà nội",),
		),
		Scenario(
			5,
			"Episodic recall: completed administrative task",
			[
				"Đã xong việc nộp hồ sơ hoàn phí trước bạ cho xe máy.",
				"Mình vừa hoàn tất việc gì?",
			],
			("trước bạ",),
		),
		Scenario(
			6,
			"Episodic recall: resolved complaint ticket",
			[
				"Vụ khiếu nại mã KN-8841 đã resolved xong.",
				"Mình vừa giải quyết vụ nào?",
			],
			("kn-8841",),
		),
		Scenario(
			7,
			"Semantic retrieval: complaint response SLA policy",
			[
				"Chiều nay nhớ nhắc mình ký hợp đồng thuê kho.",
				"Theo quy chế nội bộ QD-17, khiếu nại cấp 1 phải phản hồi trong bao lâu? Trả lời kèm cấp ưu tiên.",
			],
			("36 giờ", "cấp 1"),
		),
		Scenario(
			8,
			"Semantic retrieval: KYC retention policy",
			[
				"Sáng mai nhắc mình mang CCCD đi ngân hàng.",
				"Theo quy trình HT-22, hồ sơ KYC nhóm B phải lưu tối thiểu bao lâu?",
			],
			("18 tháng", "nhóm b"),
		),
		Scenario(
			9,
			"Token budget trim under long context",
			[
				"Mình tên là Vũ Hải Đăng.",
				"".join(["spam "] * 180),
				"Trả lời đúng 1 cụm ngắn: tên mình là gì?",
			],
			("vũ hải đăng",),
		),
		Scenario(
			10,
			"Combined profile + semantic in one response",
			[
				"Mình tên là Vũ Hải Đăng.",
				"Theo hướng dẫn BM-47, giao dịch treo phải hoàn tiền trong bao lâu? Nhớ gọi tên mình trước.",
			],
			("vũ hải đăng", "5 ngày làm việc"),
		),
	]


def run_benchmark(project_root: Path, use_openai: bool = True) -> str:
	scenarios = _build_scenarios()
	with_memory = MemoryAgent(project_root=project_root, enable_memory=True, use_openai=use_openai)
	no_memory = MemoryAgent(project_root=project_root, enable_memory=False, use_openai=use_openai)
	with_memory.semantic.index_documents(_build_benchmark_semantic_docs())

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

