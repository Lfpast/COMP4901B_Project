"""
Task Runner: Thesis Defense Preparation

This script runs the SearchAgent on Task 3 from part2_realistic_tasks.md.
"""

from src.agent import SearchAgent


def run_thesis_defense_preparation():
    agent = SearchAgent(
        use_tools=True,
        use_browsing=True,
        use_shopping=True,
        enable_maps=True,
        enable_scholar=True,
        max_steps=15,
    )

    user_query = """
    I'm defending my undergraduate thesis on graph neural networks for
    molecular property prediction at HKUST next week. Help me:
    1. Find 4 recent papers (2022+) that support or extend my topic, with notes
       on how each can strengthen my defense.
    2. Locate 2-3 reliable thesis printing/binding shops or poster printing
       services near HKUST (Clear Water Bay).
    3. Recommend what to buy for the defense (formal attire, presentation
       clicker, document folders, USB backup) with a total budget of HK$2500.
    Provide addresses for print shops and shopping links when possible.
    """

    print("=" * 70)
    print("Running Task 3: Thesis Defense Preparation")
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
    run_thesis_defense_preparation()

