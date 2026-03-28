import unittest
import sys
import os

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game import KBCGame, SAFE_HAVENS
from questions import load_questions, get_questions_by_difficulty, get_random_questions, get_prize_money
from leaderboard import save_score, load_leaderboard, is_high_score, reset_leaderboard
from utils import format_prize


# ─────────────────────────────────────────────
#  MOCK DATA
# ─────────────────────────────────────────────

SAMPLE_QUESTION = {
    "id": 1,
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


# ─────────────────────────────────────────────
#  TESTS — questions.py
# ─────────────────────────────────────────────

class TestQuestions(unittest.TestCase):

    def test_load_all_questions(self):
        """Should load all 15 questions."""
        questions = load_questions()
        self.assertEqual(len(questions), 15)

    def test_load_easy_questions(self):
        """Should return only easy questions."""
        questions = load_questions("easy")
        self.assertTrue(len(questions) > 0)
        for q in questions:
            self.assertEqual(q["difficulty"], "easy")

    def test_load_medium_questions(self):
        """Should return only medium questions."""
        questions = load_questions("medium")
        self.assertTrue(len(questions) > 0)
        for q in questions:
            self.assertEqual(q["difficulty"], "medium")

    def test_load_hard_questions(self):
        """Should return only hard questions."""
        questions = load_questions("hard")
        self.assertTrue(len(questions) > 0)
        for q in questions:
            self.assertEqual(q["difficulty"], "hard")

    def test_load_invalid_difficulty(self):
        """Should return empty list for invalid difficulty."""
        questions = load_questions("extreme")
        self.assertEqual(questions, [])

    def test_questions_have_required_fields(self):
        """Every question must have required fields."""
        questions = load_questions()
        required_fields = ["id", "question", "options", "answer", "prize", "difficulty"]
        for q in questions:
            for field in required_fields:
                self.assertIn(field, q, f"Missing field '{field}' in question {q.get('id')}")

    def test_questions_have_four_options(self):
        """Every question must have exactly 4 options."""
        questions = load_questions()
        for q in questions:
            self.assertEqual(len(q["options"]), 4)

    def test_answer_is_valid_option(self):
        """Answer key must be one of A, B, C, D."""
        questions = load_questions()
        for q in questions:
            self.assertIn(q["answer"], ["A", "B", "C", "D"])

    def test_get_questions_by_difficulty_order(self):
        """Questions should be ordered easy → medium → hard."""
        questions = get_questions_by_difficulty()
        difficulties = [q["difficulty"] for q in questions]
        easy_indices   = [i for i, d in enumerate(difficulties) if d == "easy"]
        medium_indices = [i for i, d in enumerate(difficulties) if d == "medium"]
        hard_indices   = [i for i, d in enumerate(difficulties) if d == "hard"]
        if easy_indices and medium_indices:
            self.assertLess(max(easy_indices), min(medium_indices))
        if medium_indices and hard_indices:
            self.assertLess(max(medium_indices), min(hard_indices))

    def test_get_random_questions_count(self):
        """Random questions should return the requested count."""
        questions = get_random_questions(5)
        self.assertEqual(len(questions), 5)

    def test_get_prize_money_format(self):
        """Prize money should be formatted with ₹ symbol."""
        prize = get_prize_money(SAMPLE_QUESTION)
        self.assertTrue(prize.startswith("₹"))


# ─────────────────────────────────────────────
#  TESTS — game.py
# ─────────────────────────────────────────────

class TestKBCGame(unittest.TestCase):

    def setUp(self):
        """Create a fresh game instance before each test."""
        self.game = KBCGame("TestPlayer")

    def test_initial_prize_is_zero(self):
        """Prize should start at 0."""
        self.assertEqual(self.game.prize_won, 0)

    def test_initial_index_is_zero(self):
        """Game should start at question 0."""
        self.assertEqual(self.game.current_index, 0)

    def test_game_not_over_at_start(self):
        """Game should not be over at the start."""
        self.assertFalse(self.game.game_over)

    def test_all_lifelines_available_at_start(self):
        """All 3 lifelines should be available at start."""
        available = self.game.get_available_lifelines()
        self.assertEqual(len(available), 3)

    def test_correct_answer_returns_true(self):
        """Correct answer should return True."""
        question = self.game.get_current_question()
        correct = question["answer"]
        self.assertTrue(self.game.check_answer(correct))

    def test_wrong_answer_returns_false(self):
        """Wrong answer should return False."""
        question = self.game.get_current_question()
        correct = question["answer"]
        wrong = [opt for opt in ["A", "B", "C", "D"] if opt != correct][0]
        self.assertFalse(self.game.check_answer(wrong))

    def test_answer_is_case_insensitive(self):
        """Answer check should be case-insensitive."""
        question = self.game.get_current_question()
        correct = question["answer"].lower()
        self.assertTrue(self.game.check_answer(correct))

    def test_advance_increments_index(self):
        """Advancing should move to the next question."""
        self.game.advance()
        self.assertEqual(self.game.current_index, 1)

    def test_advance_updates_prize(self):
        """Advancing should update prize_won."""
        self.game.advance()
        self.assertGreater(self.game.prize_won, 0)

    def test_safe_haven_updated_at_checkpoint(self):
        """Safe haven should update at checkpoint questions."""
        for i in range(SAFE_HAVENS[0] + 1):
            self.game.advance()
        self.assertGreater(self.game.safe_haven_amount, 0)

    def test_use_lifeline_marks_as_used(self):
        """Using a lifeline should mark it as unavailable."""
        self.game.use_lifeline("50-50")
        self.assertFalse(self.game.lifelines["50-50"])

    def test_use_lifeline_twice_returns_false(self):
        """Using a lifeline twice should return False."""
        self.game.use_lifeline("50-50")
        result = self.game.use_lifeline("50-50")
        self.assertFalse(result)

    def test_available_lifelines_decreases_after_use(self):
        """Available lifelines count should decrease after use."""
        self.game.use_lifeline("50-50")
        available = self.game.get_available_lifelines()
        self.assertEqual(len(available), 2)

    def test_game_over_after_all_questions(self):
        """Game should be over after answering all 15 questions."""
        for _ in range(15):
            self.game.advance()
        self.assertTrue(self.game.game_over)
        self.assertTrue(self.game.won)

    def test_get_current_prize_format(self):
        """get_current_prize should return a ₹ formatted string."""
        prize = self.game.get_current_prize()
        self.assertTrue(prize.startswith("₹"))

    def test_quit_game_sets_game_over(self):
        """Quitting should set game_over to True."""
        self.game.quit_game()
        self.assertTrue(self.game.game_over)


# ─────────────────────────────────────────────
#  TESTS — leaderboard.py
# ─────────────────────────────────────────────

class TestLeaderboard(unittest.TestCase):

    def setUp(self):
        """Reset leaderboard before each test."""
        import os
        from leaderboard import LEADERBOARD_FILE
        if os.path.exists(LEADERBOARD_FILE):
            os.remove(LEADERBOARD_FILE)

    def test_save_and_load_score(self):
        """Saved score should appear in leaderboard."""
        save_score("Aditya", 100000)
        leaderboard = load_leaderboard()
        self.assertEqual(len(leaderboard), 1)
        self.assertEqual(leaderboard[0]["name"], "Aditya")
        self.assertEqual(leaderboard[0]["prize"], 100000)

    def test_leaderboard_sorted_by_prize(self):
        """Leaderboard should be sorted highest prize first."""
        save_score("Player1", 10000)
        save_score("Player2", 500000)
        save_score("Player3", 100000)
        leaderboard = load_leaderboard()
        prizes = [entry["prize"] for entry in leaderboard]
        self.assertEqual(prizes, sorted(prizes, reverse=True))

    def test_leaderboard_max_10_entries(self):
        """Leaderboard should never exceed 10 entries."""
        for i in range(15):
            save_score(f"Player{i}", i * 1000)
        leaderboard = load_leaderboard()
        self.assertLessEqual(len(leaderboard), 10)

    def test_is_high_score_empty_board(self):
        """Any score should qualify on an empty leaderboard."""
        self.assertTrue(is_high_score(100))

    def test_score_has_formatted_prize(self):
        """Saved entry should have a formatted prize string."""
        save_score("Aditya", 50000)
        leaderboard = load_leaderboard()
        self.assertIn("₹", leaderboard[0]["prize_formatted"])

    def test_score_has_date(self):
        """Saved entry should have a date field."""
        save_score("Aditya", 50000)
        leaderboard = load_leaderboard()
        self.assertIn("date", leaderboard[0])


# ─────────────────────────────────────────────
#  TESTS — utils.py
# ─────────────────────────────────────────────

class TestUtils(unittest.TestCase):

    def test_format_prize_small(self):
        """Small prize should format correctly."""
        self.assertEqual(format_prize(1000), "₹1,000")

    def test_format_prize_large(self):
        """Large prize should format correctly."""
        self.assertEqual(format_prize(10000000), "₹10,000,000")

    def test_format_prize_zero(self):
        """Zero prize should format correctly."""
        self.assertEqual(format_prize(0), "₹0")


# ─────────────────────────────────────────────
#  RUN ALL TESTS
# ─────────────────────────────────────────────

if __name__ == "__main__":
    unittest.main(verbosity=2)