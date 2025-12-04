"""
Task Runner: AI Conference Preparation

This script runs the SearchAgent on Task 1 from part2_realistic_tasks.md:
preparing for an AI conference attendance with literature review, hotel
planning, and equipment shopping requirements.
"""

from src.agent import SearchAgent


def run_conference_preparation():
    agent = SearchAgent(
        use_tools=True,
        use_browsing=True,
        use_shopping=True,
        enable_maps=True,
        enable_scholar=True,
        max_steps=15,
    )

    user_query = """
    I will attend a multimodal AI conference in Kowloon next month.
    Please:
    1. Suggest 3-5 recent papers (>=2022) on multimodal learning to read beforehand.
    2. Find 2 nearby hotels within a 15-minute walk from the Kowloon MTR area,
       with good ratings and business-friendly amenities (Wi-Fi, workspace).
    3. Recommend conference essentials to buy (voice recorder, portable charger,
       business card holder, notebook) with a total budget under HK$1200.
    Provide concrete hotel names, addresses, and shopping links when possible.
    """

    print("=" * 70)
    print("Running Task 1: Conference Preparation")
    print("=" * 70)

    result = agent.solve(user_query)

    print_reasoning_and_tools(result)
    print_final_answer(result)

    return result


def print_reasoning_and_tools(result):
    print("\n" + "=" * 70)
    print("Reasoning Steps")
    print("=" * 70)
    for step in result.get("reasoning_steps", []):
        step_no = step.get("step", "?")
        content = step.get("content", "")
        print(f"\nStep {step_no}: {content}")

    print("\n" + "=" * 70)
    print("Tool Calls")
    print("=" * 70)
    for idx, call in enumerate(result.get("tool_calls", []), 1):
        print(f"\nTool Call {idx}:")
        for key, value in call.items():
            if key == "result":
                truncated = value if len(value) < 300 else value[:300] + "..."
                print(f"  {key}: {truncated}")
            else:
                print(f"  {key}: {value}")


def print_final_answer(result):
    print("\n" + "=" * 70)
    print("Final Answer")
    print("=" * 70)
    print(result.get("final_answer", "(no final answer returned)"))


if __name__ == "__main__":
    run_conference_preparation()

