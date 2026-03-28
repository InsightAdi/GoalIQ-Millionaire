import json
import os
import random


def load_questions(difficulty=None):
    """
    Load questions from the JSON file.
    
    Args:
        difficulty (str): Filter by 'easy', 'medium', 'hard', or None for all questions.
    
    Returns:
        list: A list of question dictionaries.
    """
    # Build the path to the JSON file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data", "questions.json")

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: questions.json not found at {file_path}")
        return []

    # Load the JSON file
    with open(file_path, "r") as f:
        all_questions = json.load(f)

    # Filter by difficulty if provided
    if difficulty:
        difficulty = difficulty.lower()
        filtered = [q for q in all_questions if q["difficulty"] == difficulty]

        if not filtered:
            print(f"No questions found for difficulty: {difficulty}")
            return []

        return filtered

    return all_questions


def get_questions_by_difficulty():
    """
    Load all questions sorted by difficulty: easy → medium → hard.
    This is used for the main KBC game flow.

    Returns:
        list: Questions sorted in KBC order (easy to hard).
    """
    easy = load_questions("easy")
    medium = load_questions("medium")
    hard = load_questions("hard")

    return easy + medium + hard


def get_random_questions(count=15):
    """
    Load random questions from the full question bank.

    Args:
        count (int): Number of random questions to return.

    Returns:
        list: A randomly selected list of questions.
    """
    all_questions = load_questions()

    if len(all_questions) < count:
        print(f"Warning: Only {len(all_questions)} questions available.")
        return all_questions

    return random.sample(all_questions, count)


def display_question(question):
    """
    Display a single question with its options in a formatted way.

    Args:
        question (dict): A question dictionary.
    """
    print(f"\n  {question['question']}")
    print("-" * 50)
    for key, value in question["options"].items():
        print(f"  {key}) {value}")
    print("-" * 50)


def get_prize_money(question):
    """
    Get formatted prize money for a question.

    Args:
        question (dict): A question dictionary.

    Returns:
        str: Prize money formatted with commas (e.g. ₹10,000).
    """
    return f"₹{int(question['prize']):,}"


# ✅ Test the functions when running this file directly
if __name__ == "__main__":
    print("=" * 50)
    print("        Testing questions.py")
    print("=" * 50)

    # Test 1: Load all questions
    all_q = load_questions()
    print(f"\n✅ Total questions loaded: {len(all_q)}")

    # Test 2: Load by difficulty
    easy_q = load_questions("easy")
    medium_q = load_questions("medium")
    hard_q = load_questions("hard")
    print(f"✅ Easy: {len(easy_q)} | Medium: {len(medium_q)} | Hard: {len(hard_q)}")

    # Test 3: Display first question
    print("\n✅ Sample Question:")
    display_question(all_q[0])
    print(f"   Prize: {get_prize_money(all_q[0])}")

    # Test 4: Get questions in KBC order
    kbc_q = get_questions_by_difficulty()
    print(f"\n✅ KBC order questions: {len(kbc_q)}")
    for q in kbc_q:
        print(f"   Q{q['id']} | {q['difficulty'].upper()} | {get_prize_money(q)} | {q['question'][:40]}...")