from questions import get_questions_by_difficulty, display_question, get_prize_money


# Prize ladder for reference display
PRIZE_LADDER = [
    "₹1,000", "₹2,000", "₹3,000", "₹5,000", "₹10,000",
    "₹20,000", "₹40,000", "₹80,000", "₹1,60,000", "₹3,20,000",
    "₹6,40,000", "₹12,50,000", "₹25,00,000", "₹50,00,000", "₹1,00,00,000"
]

# Safe havens — player keeps this amount even if they lose after this point
SAFE_HAVENS = [4, 9]  # Question index (0-based) → Q5 and Q10


class KBCGame:
    def __init__(self, player_name):
        """
        Initialize the KBC game.

        Args:
            player_name (str): Name of the player.
        """
        self.player_name = player_name
        self.questions = get_questions_by_difficulty()
        self.current_index = 0
        self.prize_won = 0
        self.safe_haven_amount = 0
        self.game_over = False
        self.won = False
        self.lifelines = {
            "50-50": True,
            "audience_poll": True,
            "phone_a_friend": True
        }

    def get_current_question(self):
        """Returns the current question."""
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    def check_answer(self, user_answer):
        """
        Check if the user's answer is correct.

        Args:
            user_answer (str): The answer chosen by the player (A/B/C/D).

        Returns:
            bool: True if correct, False otherwise.
        """
        question = self.get_current_question()
        if not question:
            return False
        return user_answer.upper() == question["answer"].upper()

    def advance(self):
        """
        Move to the next question and update prize + safe haven.
        """
        question = self.get_current_question()
        if question:
            self.prize_won = int(question["prize"])

            # Update safe haven if current question is a checkpoint
            if self.current_index in SAFE_HAVENS:
                self.safe_haven_amount = self.prize_won

        self.current_index += 1

        # Check if all questions are answered
        if self.current_index >= len(self.questions):
            self.won = True
            self.game_over = True

    def use_lifeline(self, lifeline_name):
        """
        Mark a lifeline as used.

        Args:
            lifeline_name (str): Name of the lifeline used.

        Returns:
            bool: True if lifeline was available, False if already used.
        """
        if self.lifelines.get(lifeline_name):
            self.lifelines[lifeline_name] = False
            return True
        print(f"  ⚠️  Lifeline '{lifeline_name}' already used!")
        return False

    def quit_game(self):
        """Player chooses to quit and take current winnings."""
        self.game_over = True
        print(f"\n  You chose to quit. You walk away with {self.get_current_prize()}! 🏆")

    def get_current_prize(self):
        """Returns current prize as a formatted string."""
        return f"₹{self.prize_won:,}"

    def get_safe_haven(self):
        """Returns safe haven amount as a formatted string."""
        return f"₹{self.safe_haven_amount:,}"

    def get_available_lifelines(self):
        """Returns list of available (unused) lifelines."""
        return [name for name, available in self.lifelines.items() if available]

    def display_prize_ladder(self):
        """Display the prize ladder with current position highlighted."""
        print("\n  📊 PRIZE LADDER")
        print("  " + "=" * 30)
        for i in range(len(PRIZE_LADDER) - 1, -1, -1):
            marker = "👉" if i == self.current_index else "  "
            safe = "🔒" if i in SAFE_HAVENS else "  "
            print(f"  {marker} Q{i+1:02d}  {PRIZE_LADDER[i]:<15} {safe}")
        print("  " + "=" * 30)

    def display_status(self):
        """Display current game status."""
        print(f"\n  🏆 Prize so far  : {self.get_current_prize()}")
        print(f"  🔒 Safe haven   : {self.get_safe_haven()}")
        available = self.get_available_lifelines()
        if available:
            lifeline_display = {
                "50-50": "5️⃣0️⃣-5️⃣0️⃣",
                "audience_poll": "👥 Audience Poll",
                "phone_a_friend": "📞 Phone a Friend"
            }
            icons = [lifeline_display[l] for l in available]
            print(f"  🎯 Lifelines    : {' | '.join(icons)}")
        else:
            print("  🎯 Lifelines    : None remaining")


def play_kbc():
    """Main function to run the KBC Football Quiz game."""

    print("\n" + "=" * 55)
    print("  🏆  KAUN BANEGA CROREPATI — FOOTBALL EDITION  🏆")
    print("=" * 55)
    print("  Answer 15 football questions to win ₹1,00,00,000!")
    print("  Safe havens at Q5 (₹10,000) and Q10 (₹3,20,000)")
    print("=" * 55)

    # Get player name
    try:
        player_name = input("\n  Enter your name: ").strip()
        if not player_name:
            player_name = "Player"
    except KeyboardInterrupt:
        print("\n  Game cancelled.")
        return

    print(f"\n  Welcome, {player_name}! Let's play! ⚽\n")

    # Initialize game
    game = KBCGame(player_name)

    while not game.game_over:
        question = game.get_current_question()
        if not question:
            break

        # Display question header
        print("\n" + "=" * 55)
        print(f"  ❓ Question {game.current_index + 1} of 15  |  Prize: {get_prize_money(question)}")
        print("=" * 55)

        # Display current status
        game.display_status()

        # Display the question
        display_question(question)

        # Show lifeline options if available
        available_lifelines = game.get_available_lifelines()
        if available_lifelines:
            print("\n  Type L to use a lifeline, P for prize ladder, Q to quit")
        else:
            print("\n  Type P for prize ladder, Q to quit")

        # Get player input
        while True:
            try:
                user_input = input("\n  Your answer (A/B/C/D): ").strip().upper()
            except KeyboardInterrupt:
                print("\n  Game cancelled.")
                return

            # Handle quit
            if user_input == "Q":
                game.quit_game()
                break

            # Handle prize ladder
            elif user_input == "P":
                game.display_prize_ladder()
                continue

            # Handle lifeline
            elif user_input == "L":
                if not available_lifelines:
                    print("  ⚠️  No lifelines remaining!")
                    continue

                print("\n  Available lifelines:")
                lifeline_map = {}
                for i, lifeline in enumerate(available_lifelines, 1):
                    lifeline_display = {
                        "50-50": "50-50 (removes 2 wrong options)",
                        "audience_poll": "Audience Poll (shows poll %)",
                        "phone_a_friend": "Phone a Friend (gives a hint)"
                    }
                    print(f"  {i}. {lifeline_display[lifeline]}")
                    lifeline_map[str(i)] = lifeline

                try:
                    choice = input("\n  Choose lifeline (number): ").strip()
                    if choice in lifeline_map:
                        chosen = lifeline_map[choice]
                        from lifelines import use_lifeline
                        use_lifeline(game, question, chosen)
                    else:
                        print("  Invalid choice.")
                except KeyboardInterrupt:
                    print("\n  Game cancelled.")
                    return
                continue

            # Handle answer
            elif user_input in ["A", "B", "C", "D"]:
                print(f"\n  ⏳ Your answer: {user_input}... ", end="", flush=True)

                import time
                time.sleep(1)

                if game.check_answer(user_input):
                    print("✅ CORRECT!")
                    print(f"  🎉 You've won {get_prize_money(question)}!")

                    # Check safe haven message
                    if game.current_index in SAFE_HAVENS:
                        print(f"  🔒 Safe haven reached! ₹{int(question['prize']):,} is guaranteed!")

                    game.advance()
                else:
                    correct = question["answer"]
                    correct_text = question["options"][correct]
                    print("❌ WRONG!")
                    print(f"  The correct answer was: {correct}) {correct_text}")
                    print(f"\n  😢 Game over, {player_name}!")
                    print(f"  You walk away with: {game.get_safe_haven()} 🔒")
                    game.game_over = True
                break

            else:
                print("  ⚠️  Invalid input! Enter A, B, C, D, L, P, or Q.")

    # Game end screen
    print("\n" + "=" * 55)
    if game.won:
        print("  🏆🏆🏆 CONGRATULATIONS! 🏆🏆🏆")
        print(f"  {player_name}, you've won ₹1,00,00,000!")
        print("  You are a TRUE Football Legend! ⚽🌟")
    else:
        print(f"  Thanks for playing, {player_name}!")
        print(f"  Final winnings: {game.get_current_prize()}")
    print("=" * 55 + "\n")

    # Save score to leaderboard
    try:
        from leaderboard import save_score
        save_score(player_name, game.prize_won)
        print("  ✅ Score saved to leaderboard!")
    except ImportError:
        pass


if __name__ == "__main__":
    play_kbc()