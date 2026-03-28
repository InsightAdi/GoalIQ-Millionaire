from game import play_kbc
from leaderboard import display_leaderboard
from utils import clear_screen, print_header, get_valid_answer, get_yes_no


def main_menu():
    """
    Display the main menu and handle navigation.
    """
    while True:
        clear_screen()

        print("\n")
        print("  ⚽  ⚽  ⚽  ⚽  ⚽  ⚽  ⚽  ⚽  ⚽  ⚽")
        print()
        print("     🏆  KAUN BANEGA CROREPATI  🏆")
        print("          — FOOTBALL EDITION —")
        print()
        print("  ⚽  ⚽  ⚽  ⚽  ⚽  ⚽  ⚽  ⚽  ⚽  ⚽")
        print()
        print_header("MAIN MENU")
        print()
        print("    1️⃣   Play Game")
        print("    2️⃣   View Leaderboard")
        print("    3️⃣   How to Play")
        print("    4️⃣   Quit")
        print()

        choice = get_valid_answer(
            prompt="  Enter your choice (1/2/3/4): ",
            allowed=["1", "2", "3", "4"]
        )

        if choice == "1":
            clear_screen()
            play_kbc()
            input("\n  Press Enter to return to the main menu...")

        elif choice == "2":
            clear_screen()
            display_leaderboard()
            input("\n  Press Enter to return to the main menu...")

        elif choice == "3":
            clear_screen()
            how_to_play()
            input("\n  Press Enter to return to the main menu...")

        elif choice == "4":
            clear_screen()
            print("\n  👋  Thanks for playing Football KBC!")
            print("  See you on the pitch! ⚽\n")
            break


def how_to_play():
    """
    Display game instructions.
    """
    print_header("HOW TO PLAY")
    print()
    print("  🎯  OBJECTIVE")
    print("      Answer 15 football questions correctly")
    print("      to win ₹1,00,00,000!")
    print()
    print("  📋  RULES")
    print("      • Each question has 4 options (A, B, C, D)")
    print("      • Answer correctly to move to the next question")
    print("      • Wrong answer ends the game")
    print()
    print("  🔒  SAFE HAVENS")
    print("      • Q5  → ₹10,000   (guaranteed if you reach it)")
    print("      • Q10 → ₹3,20,000 (guaranteed if you reach it)")
    print()
    print("  🎯  LIFELINES  (each can be used only once)")
    print("      • 5️⃣0️⃣-5️⃣0️⃣  → Removes 2 wrong options")
    print("      • 👥  Audience Poll  → Shows how audience voted")
    print("      • 📞  Phone a Friend → A friend gives you a hint")
    print()
    print("  ⌨️   CONTROLS")
    print("      • A / B / C / D  → Answer the question")
    print("      • L              → Use a lifeline")
    print("      • P              → View prize ladder")
    print("      • Q              → Quit and take winnings")
    print()
    print("  🏆  PRIZE LADDER")
    prizes = [
        ("Q1",  "₹1,000"),     ("Q2",  "₹2,000"),
        ("Q3",  "₹3,000"),     ("Q4",  "₹5,000"),
        ("Q5",  "₹10,000 🔒"), ("Q6",  "₹20,000"),
        ("Q7",  "₹40,000"),    ("Q8",  "₹80,000"),
        ("Q9",  "₹1,60,000"),  ("Q10", "₹3,20,000 🔒"),
        ("Q11", "₹6,40,000"),  ("Q12", "₹12,50,000"),
        ("Q13", "₹25,00,000"), ("Q14", "₹50,00,000"),
        ("Q15", "₹1,00,00,000 🏆"),
    ]
    for i in range(0, len(prizes), 2):
        left = f"{prizes[i][0]:<4}  {prizes[i][1]:<18}"
        right = f"{prizes[i+1][0]:<4}  {prizes[i+1][1]}" if i + 1 < len(prizes) else ""
        print(f"      {left}  {right}")
    print()


if __name__ == "__main__":
    main_menu()