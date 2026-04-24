"""Interactive entrypoint for the memory agent."""

from __future__ import annotations

from pathlib import Path

from src.agent import MemoryAgent


def run_cli() -> None:
	root = Path(__file__).resolve().parents[1]
	agent = MemoryAgent(project_root=root, enable_memory=True, use_openai=True)
	user_id = "demo_user"

	print("Memory Agent CLI. Type 'exit' to quit.")
	while True:
		text = input("You: ").strip()
		if text.lower() in {"exit", "quit"}:
			print("Bye")
			break
		reply = agent.chat(user_id=user_id, user_message=text, memory_budget=220)
		print(f"Agent: {reply}")


if __name__ == "__main__":
	run_cli()

