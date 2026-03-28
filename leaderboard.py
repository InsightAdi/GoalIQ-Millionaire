import json
import os
from datetime import datetime


# Path to leaderboard file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEADERBOARD_FILE = os.path.join(BASE_DIR, "data", "leaderboard.json")

# Maximum entries to keep on leaderboard
MAX_ENTRIES = 10


# ─────────────────────────────────────────────
#  SAVE SCORE
# ─────────────────────────────────────────────

def save_score(player_name, prize_won):
    """
    Save a player's score to the leaderboard.

    Args:
        player_name (str): Name of the player.
        prize_won (int)  : Prize amount won by the player.
    """
    leaderboard = load_leaderboard()

    # Create new entry
    new_entry = {
        "name": player_name,
        "prize": prize_won,
        "prize_formatted": f"₹{prize_won:,}",
        "date": datetime.now().strftime("%d %b %Y"),
        "time": datetime.now().strftime("%I:%M %p")
    }

    leaderboard.append(new_entry)

    # Sort by prize (highest first) and keep top MAX_ENTRIES
    leaderboard = sorted(leaderboard, key=lambda x: x["prize"], reverse=True)
    leaderboard = leaderboard[:MAX_ENTRIES]

    # Save back to file
    os.makedirs(os.path.dirname(LEADERBOARD_FILE), exist_ok=True)
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f, indent=4)

    print(f"\n  ✅ Score saved for {player_name}: ₹{prize_won:,}")


# ─────────────────────────────────────────────
#  LOAD LEADERBOARD
# ─────────────────────────────────────────────

def load_leaderboard():
    """
    Load the leaderboard from the JSON file.

    Returns:
        list: List of leaderboard entry dictionaries.
    """
    if not os.path.exists(LEADERBOARD_FILE):
        return []

    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        print("  ⚠️  Leaderboard file corrupted. Starting fresh.")
        return []


# ─────────────────────────────────────────────
#  DISPLAY LEADERBOARD
# ─────────────────────────────────────────────

def display_leaderboard():
    """
    Display the top 10 leaderboard in a formatted table.
    """
    leaderboard = load_leaderboard()

    print("\n" + "=" * 55)
    print("       🏆  FOOTBALL KBC — HALL OF FAME  🏆")
    print("=" * 55)

    if not leaderboard:
        print("  No scores yet. Be the first to play!")
        print("=" * 55)
        return

    # Medal icons for top 3
    medals = {0: "🥇", 1: "🥈", 2: "🥉"}

    print(f"  {'Rank':<5} {'Name':<18} {'Prize':<16} {'Date'}")
    print("  " + "─" * 50)

    for i, entry in enumerate(leaderboard):
        rank = medals.get(i, f"#{i + 1} ")
        name = entry["name"][:16]                   # Truncate long names
        prize = entry["prize_formatted"]
        date = entry.get("date", "N/A")
        print(f"  {rank:<5} {name:<18} {prize:<16} {date}")

    print("=" * 55)


# ─────────────────────────────────────────────
#  CHECK IF PLAYER IS IN TOP 10
# ─────────────────────────────────────────────

def is_high_score(prize_won):
    """
    Check if a score qualifies for the leaderboard.

    Args:
        prize_won (int): Prize amount to check.

    Returns:
        bool: True if it's a top 10 score.
    """
    leaderboard = load_leaderboard()

    if len(leaderboard) < MAX_ENTRIES:
        return True

    lowest = min(entry["prize"] for entry in leaderboard)
    return prize_won > lowest


# ─────────────────────────────────────────────
#  RESET LEADERBOARD
# ─────────────────────────────────────────────

def reset_leaderboard():
    """
    Clear all leaderboard entries. Use with caution!
    """
    confirm = input("\n  ⚠️  Are you sure you want to reset the leaderboard? (yes/no): ").strip().lower()
    if confirm == "yes":
        if os.path.exists(LEADERBOARD_FILE):
            os.remove(LEADERBOARD_FILE)
        print("  ✅ Leaderboard has been reset.")
    else:
        print("  ❌ Reset cancelled.")


# ─────────────────────────────────────────────
#  QUICK TEST
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("        Testing leaderboard.py")
    print("=" * 55)

    # Test 1: Save some scores
    print("\n✅ TEST 1 — Saving scores")
    save_score("Aditya", 1000000)
    save_score("Rahul", 320000)
    save_score("Priya", 10000000)
    save_score("Carlos", 80000)
    save_score("Sofia", 640000)

    # Test 2: Display leaderboard
    print("\n✅ TEST 2 — Display leaderboard")
    display_leaderboard()

    # Test 3: Check high score
    print("\n✅ TEST 3 — High score check")
    print(f"  Is ₹5,00,000 a high score? {is_high_score(500000)}")
    print(f"  Is ₹100 a high score? {is_high_score(100)}")

    # Test 4: Reset leaderboard
    print("\n✅ TEST 4 — Reset leaderboard")
    reset_leaderboard()