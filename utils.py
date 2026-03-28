import time
import threading
import sys


# ─────────────────────────────────────────────
#  TIMER
# ─────────────────────────────────────────────

class QuestionTimer:
    """
    A countdown timer that runs in a background thread.
    Displays remaining seconds inline without blocking input.
    """

    def __init__(self, seconds=30):
        self.seconds = seconds
        self.time_left = seconds
        self.expired = False
        self._thread = None
        self._stop_event = threading.Event()

    def start(self):
        """Start the countdown timer in a background thread."""
        self._stop_event.clear()
        self.expired = False
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the timer (called when player answers)."""
        self._stop_event.set()

    def _run(self):
        """Internal countdown loop."""
        for i in range(self.seconds, 0, -1):
            if self._stop_event.is_set():
                return
            self.time_left = i
            print(f"\r  ⏱️  Time left: {i:02d}s  ", end="", flush=True)
            time.sleep(1)

        # Time ran out
        if not self._stop_event.is_set():
            self.expired = True
            print(f"\r  ⏱️  Time's up! ❌              ")


# ─────────────────────────────────────────────
#  INPUT VALIDATION
# ─────────────────────────────────────────────

def get_valid_answer(prompt="  Your answer (A/B/C/D): ", allowed=None):
    """
    Keep prompting until the user enters a valid input.

    Args:
        prompt (str) : The input prompt to display.
        allowed (list): List of valid inputs. Defaults to A/B/C/D + L/P/Q.

    Returns:
        str: Validated uppercase input from the user.
    """
    if allowed is None:
        allowed = ["A", "B", "C", "D", "L", "P", "Q"]

    while True:
        try:
            user_input = input(prompt).strip().upper()
            if user_input in allowed:
                return user_input
            print(f"  ⚠️  Invalid input! Please enter one of: {', '.join(allowed)}")
        except KeyboardInterrupt:
            print("\n  Game cancelled.")
            sys.exit(0)


def get_valid_name(prompt="  Enter your name: "):
    """
    Prompt for a player name and ensure it's not empty.

    Args:
        prompt (str): The input prompt to display.

    Returns:
        str: A non-empty player name.
    """
    while True:
        try:
            name = input(prompt).strip()
            if name:
                return name
            print("  ⚠️  Name cannot be empty. Please try again.")
        except KeyboardInterrupt:
            print("\n  Game cancelled.")
            sys.exit(0)


def get_yes_no(prompt):
    """
    Prompt for a yes/no answer.

    Args:
        prompt (str): The question to ask.

    Returns:
        bool: True for yes, False for no.
    """
    while True:
        try:
            answer = input(prompt).strip().lower()
            if answer in ["y", "yes"]:
                return True
            elif answer in ["n", "no"]:
                return False
            print("  ⚠️  Please enter yes or no.")
        except KeyboardInterrupt:
            print("\n  Game cancelled.")
            sys.exit(0)


# ─────────────────────────────────────────────
#  FORMATTING HELPERS
# ─────────────────────────────────────────────

def format_prize(amount):
    """
    Format a prize amount as a rupee string with commas.

    Args:
        amount (int): Prize amount in rupees.

    Returns:
        str: Formatted string like ₹10,00,000
    """
    return f"₹{amount:,}"


def print_divider(char="=", length=55):
    """Print a divider line."""
    print("  " + char * length)


def print_header(title):
    """Print a formatted section header."""
    print_divider()
    padding = (55 - len(title)) // 2
    print("  " + " " * padding + title)
    print_divider()


def slow_print(text, delay=0.03):
    """
    Print text character by character for a dramatic effect.

    Args:
        text (str)  : Text to print slowly.
        delay (float): Delay between each character in seconds.
    """
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def dramatic_pause(seconds=1.5):
    """
    Pause with animated dots for dramatic effect.

    Args:
        seconds (float): Total pause duration.
    """
    steps = 3
    interval = seconds / steps
    for _ in range(steps):
        print(".", end="", flush=True)
        time.sleep(interval)
    print()


# ─────────────────────────────────────────────
#  CLEAR SCREEN
# ─────────────────────────────────────────────

def clear_screen():
    """Clear the terminal screen."""
    import os
    os.system("cls" if os.name == "nt" else "clear")


# ─────────────────────────────────────────────
#  GAME INTRO ANIMATION
# ─────────────────────────────────────────────

def play_intro():
    """Display an animated intro for the game."""
    clear_screen()
    print("\n")
    time.sleep(0.3)

    lines = [
        "  ⚽  ⚽  ⚽  ⚽  ⚽  ⚽  ⚽  ⚽  ⚽  ⚽",
        "",
        "     KAUN BANEGA CROREPATI",
        "       — FOOTBALL EDITION —",
        "",
        "  ⚽  ⚽  ⚽  ⚽  ⚽  ⚽  ⚽  ⚽  ⚽  ⚽",
    ]

    for line in lines:
        slow_print(line, delay=0.02)
        time.sleep(0.1)

    time.sleep(0.5)


# ─────────────────────────────────────────────
#  QUICK TEST
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("         Testing utils.py")
    print("=" * 55)

    # Test 1: format_prize
    print("\n✅ TEST 1 — format_prize")
    print(f"  {format_prize(1000)}")
    print(f"  {format_prize(100000)}")
    print(f"  {format_prize(10000000)}")

    # Test 2: print_header
    print("\n✅ TEST 2 — print_header")
    print_header("FOOTBALL KBC")

    # Test 3: slow_print
    print("\n✅ TEST 3 — slow_print")
    slow_print("  Loading your football quiz...", delay=0.03)

    # Test 4: dramatic_pause
    print("\n✅ TEST 4 — dramatic_pause")
    print("  Suspense", end="")
    dramatic_pause(1.5)

    # Test 5: Timer (runs for 5 seconds)
    print("\n✅ TEST 5 — QuestionTimer (5 seconds)")
    timer = QuestionTimer(seconds=5)
    timer.start()
    time.sleep(5)
    print(f"\n  Timer expired: {timer.expired}")

    # Test 6: Input validation
    print("\n✅ TEST 6 — get_valid_answer")
    print("  Try entering an invalid input first, then a valid one (A/B/C/D):")
    answer = get_valid_answer()
    print(f"  You entered: {answer}")