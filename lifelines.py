import random


# ─────────────────────────────────────────────
#  LIFELINE ROUTER
# ─────────────────────────────────────────────

def use_lifeline(game, question, lifeline_name):
    """
    Route to the correct lifeline function.

    Args:
        game (KBCGame)   : The current game instance.
        question (dict)  : The current question dictionary.
        lifeline_name (str): One of '50-50', 'audience_poll', 'phone_a_friend'.
    """
    if not game.use_lifeline(lifeline_name):
        return  # Already used — message handled inside use_lifeline()

    print("\n" + "─" * 50)

    if lifeline_name == "50-50":
        fifty_fifty(question)

    elif lifeline_name == "audience_poll":
        audience_poll(question)

    elif lifeline_name == "phone_a_friend":
        phone_a_friend(question)

    print("─" * 50)


# ─────────────────────────────────────────────
#  LIFELINE 1 — 50 / 50
# ─────────────────────────────────────────────

def fifty_fifty(question):
    """
    Remove two incorrect options, leaving the correct answer
    and one random wrong option.

    Args:
        question (dict): The current question dictionary.
    """
    print("  5️⃣0️⃣-5️⃣0️⃣  FIFTY-FIFTY LIFELINE")
    print("  Two wrong options have been removed!\n")

    correct = question["answer"]
    all_options = list(question["options"].keys())          # ['A','B','C','D']

    wrong_options = [opt for opt in all_options if opt != correct]
    # Keep one random wrong option, remove the other two
    keep_wrong = random.choice(wrong_options)

    surviving = sorted([correct, keep_wrong])               # always sorted A→D

    for key in surviving:
        print(f"  {key}) {question['options'][key]}")


# ─────────────────────────────────────────────
#  LIFELINE 2 — AUDIENCE POLL
# ─────────────────────────────────────────────

def audience_poll(question):
    """
    Simulate an audience poll. The correct answer gets the
    highest percentage; the rest are distributed randomly.

    Args:
        question (dict): The current question dictionary.
    """
    print("  👥  AUDIENCE POLL LIFELINE")
    print("  The audience has voted!\n")

    correct = question["answer"]
    all_options = list(question["options"].keys())
    wrong_options = [opt for opt in all_options if opt != correct]

    # Correct answer gets 45–75 % of the vote
    correct_pct = random.randint(45, 75)

    # Distribute the remainder among wrong options
    remaining = 100 - correct_pct
    split1 = random.randint(5, remaining - 10)
    split2 = random.randint(5, remaining - split1 - 5)
    split3 = remaining - split1 - split2

    wrong_pcts = sorted([split1, split2, split3], reverse=True)

    poll = {opt: pct for opt, pct in zip(wrong_options, wrong_pcts)}
    poll[correct] = correct_pct

    # Display bar chart in terminal
    print(f"  {'Option':<6} {'Votes':>6}   {'Bar'}")
    print(f"  {'─'*6}   {'─'*6}   {'─'*20}")
    for key in sorted(poll.keys()):
        bar = "█" * (poll[key] // 5)
        print(f"  {key})     {poll[key]:>3}%    {bar}")


# ─────────────────────────────────────────────
#  LIFELINE 3 — PHONE A FRIEND
# ─────────────────────────────────────────────

# A pool of football expert friends to call
FRIENDS = [
    {"name": "Rahul",   "expertise": "World Cup history buff"},
    {"name": "Priya",   "expertise": "Premier League expert"},
    {"name": "Carlos",  "expertise": "La Liga & Champions League fan"},
    {"name": "Arjun",   "expertise": "Football stats geek"},
    {"name": "Sofia",   "expertise": "UEFA & FIFA trivia master"},
]

# Confidence phrases mapped to probability level
CONFIDENCE = {
    "high":   ["I'm 100% sure it's", "Definitely", "No doubt, it's",
               "Trust me, the answer is", "I'm certain it's"],
    "medium": ["I think it's", "Pretty sure it's", "I'd go with",
               "If I had to guess, I'd say", "I believe it's"],
    "low":    ["I'm not totally sure but maybe", "Could be",
               "I'm guessing", "Not confident but possibly",
               "I'd say maybe"],
}


def phone_a_friend(question):
    """
    Simulate a 'Phone a Friend' lifeline. The friend gives a hint
    with varying confidence (correct answer 80 % of the time).

    Args:
        question (dict): The current question dictionary.
    """
    friend = random.choice(FRIENDS)
    correct = question["answer"]
    all_options = list(question["options"].keys())

    print(f"  📞  PHONE A FRIEND LIFELINE")
    print(f"  Calling {friend['name']} ({friend['expertise']})...\n")

    import time
    time.sleep(1)

    # 80 % chance the friend gives the correct answer
    gives_correct = random.random() < 0.80

    if gives_correct:
        suggested = correct
        confidence_level = random.choice(["high", "medium"])
    else:
        wrong_opts = [opt for opt in all_options if opt != correct]
        suggested = random.choice(wrong_opts)
        confidence_level = "low"

    phrase = random.choice(CONFIDENCE[confidence_level])
    answer_text = question["options"][suggested]

    print(f"  {friend['name']}: \"{phrase} {suggested}) {answer_text}.\"")

    # Friendly disclaimer
    if confidence_level == "low":
        print(f"  ⚠️  {friend['name']} doesn't sound very confident!")
    elif confidence_level == "high":
        print(f"  ✅  {friend['name']} sounds very confident!")
    else:
        print(f"  🤔  {friend['name']} seems fairly sure.")


# ─────────────────────────────────────────────
#  QUICK TEST
# ─────────────────────────────────────────────

if __name__ == "__main__":

    # Mock question for testing
    sample_question = {
        "id": 8,
        "question": "Which club has won the most UEFA Champions League titles?",
        "options": {
            "A": "FC Barcelona",
            "B": "Bayern Munich",
            "C": "AC Milan",
            "D": "Real Madrid"
        },
        "answer": "D",
        "prize": "80000",
        "difficulty": "medium"
    }

    # Mock game object for testing
    class MockGame:
        def __init__(self):
            self.lifelines = {
                "50-50": True,
                "audience_poll": True,
                "phone_a_friend": True
            }
        def use_lifeline(self, name):
            if self.lifelines.get(name):
                self.lifelines[name] = False
                return True
            print(f"  ⚠️  '{name}' already used!")
            return False

    mock_game = MockGame()

    print("=" * 50)
    print("       Testing lifelines.py")
    print("=" * 50)

    print("\n✅ TEST 1 — 50/50")
    use_lifeline(mock_game, sample_question, "50-50")

    print("\n✅ TEST 2 — Audience Poll")
    use_lifeline(mock_game, sample_question, "audience_poll")

    print("\n✅ TEST 3 — Phone a Friend")
    use_lifeline(mock_game, sample_question, "phone_a_friend")

    print("\n✅ TEST 4 — Reusing a used lifeline")
    use_lifeline(mock_game, sample_question, "50-50")