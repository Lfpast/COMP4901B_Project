"""
Task Runner: Few-Shot Learning Course Project Preparation

This script runs the SearchAgent on Task 2 from part2_realistic_tasks.md.
"""

from src.agent import SearchAgent


def run_course_project_planning():
    agent = SearchAgent(
        use_tools=True,
        use_browsing=True,
        use_shopping=True,
        enable_maps=True,
        enable_scholar=True,
        max_steps=15,
    )

    user_query = """
    I'm planning a course project on few-shot learning this semester.
    Please help me:
    1. Find 5 impactful papers (2019+) on few-shot learning or meta-learning,
       each with a short summary and why it matters.
    2. Recommend 2-3 quiet study locations in Tsim Sha Tsui with Wi-Fi and
       power outlets (library, café, or co-working space).
    3. Suggest a shopping list of study equipment (textbook, 2TB external drive,
       portable monitor, USB-C hub) with a budget of HK$3000.
    Include addresses for the locations and purchase links when possible.
    """

    print("=" * 70)
    print("Running Task 2: Course Project Preparation")
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
    run_course_project_planning()

