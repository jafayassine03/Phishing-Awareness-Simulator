import random
import json
import os
import time

emails = [
    {
        "text": "Your bank account has been locked! Click here to verify: http://secure-bank-login.xyz",
        "type": "phishing",
        "reason": "Suspicious link and urgent message.",
        "difficulty": "easy"
    },
    {
        "text": "Hi Yassine, your Amazon order has been shipped. Track here: https://amazon.com/orders",
        "type": "legit",
        "reason": "Trusted domain and no urgency tricks.",
        "difficulty": "easy"
    },
    {
        "text": "You've won a free iPhone! Claim now: http://free-iphone-win.net",
        "type": "phishing",
        "reason": "Too good to be true + fake link.",
        "difficulty": "medium"
    },
    {
        "text": "Reminder: Your university class starts at 10 AM tomorrow.",
        "type": "legit",
        "reason": "Normal message, no suspicious links.",
        "difficulty": "easy"
    },
    {
        "text": "Unusual login detected! Reset your password immediately: http://secure-reset-password.co",
        "type": "phishing",
        "reason": "Fake domain + urgency.",
        "difficulty": "medium"
    },
    {
        "text": "Dear user, we noticed unusual billing activity. Please login via https://billing-secure-paypal.com to confirm.",
        "type": "phishing",
        "reason": "Looks real but domain is fake.",
        "difficulty": "hard"
    }
]

def save_score(score, total):
    data = {"score": score, "total": total}
    
    if os.path.exists("scores.json"):
        with open("scores.json", "r") as f:
            scores = json.load(f)
    else:
        scores = []

    scores.append(data)

    with open("scores.json", "w") as f:
        json.dump(scores, f, indent=4)

def show_high_scores():
    if os.path.exists("scores.json"):
        with open("scores.json", "r") as f:
            scores = json.load(f)
        if scores:
            print("\n🏆 Previous Scores:")
            for s in scores[-5:]:
                print(f"Score: {s['score']} / {s['total']}")
        else:
            print("\nNo previous scores yet.")
    else:
        print("\nNo previous scores yet.")

def choose_difficulty():
    print("Select difficulty: easy / medium / hard")
    while True:
        choice = input("👉 ").lower()
        if choice in ["easy", "medium", "hard"]:
            return choice
        print("Invalid choice. Try again.")

def run_simulator():
    print("🔐 Phishing Awareness Simulator 🔐")
    show_high_scores()
    print("Type 'p' for phishing, 'l' for legit\n")

    difficulty = choose_difficulty()
    filtered_emails = [e for e in emails if e["difficulty"] == difficulty]

    score = 0
    lives = 3
    streak = 0
    level = 1
    power_ups = 0

    mistakes = []

    questions = random.sample(filtered_emails, len(filtered_emails))

    for i, email in enumerate(questions):
        if lives == 0:
            print("\n💀 Game Over! You're out of lives.")
            break

        time_limit = 8 

        print(f"\n📩 Message {i+1} (Level {level}):")
        print(email["text"])
        print(f"\n⏳ You have {time_limit} seconds to answer!")

        if power_ups > 0:
            print(f"\n⚡ Power-Ups available: {power_ups}")
            use = input("Use power-up? (y/n): ").lower()

            if use == "y":
                print("1. +3 seconds\n2. +1 life\n3. Show hint")
                choice = input("Choose power-up: ")

                if choice == "1":
                    time_limit += 3
                    print("⏱️ Extra time added!")
                elif choice == "2":
                    lives += 1
                    print("❤️ Extra life gained!")
                elif choice == "3":
                    print(f"💡 Hint: {email['reason']}")
                else:
                    print("Invalid choice.")

                power_ups -= 1

        start_time = time.time()
        answer = input("Is this phishing or legit? (p/l): ").lower()
        end_time = time.time()

        if end_time - start_time > time_limit:
            print("⏰ Time's up!")
            answer = "timeout"

        if answer != "timeout" and (
            (answer == "p" and email["type"] == "phishing") or
            (answer == "l" and email["type"] == "legit")
        ):
            print("✅ Correct!")
            score += 1
            streak += 1

            if streak % 2 == 0:
                power_ups += 1
                print(f"⚡ You earned a Power-Up! Total: {power_ups}")

            if streak % 3 == 0:
                level += 1
                print(f"🚀 Level Up! You reached Level {level}!")

            if streak >= 2:
                print(f"🔥 Streak: {streak} correct answers in a row!")

        else:
            lives -= 1
            print("❌ Wrong!")
            streak = 0
            print("💥 Streak reset!")
            print(f"❤️ Lives left: {lives}")
            print("💡 Hint: Look at the link carefully or consider if the offer is too good to be true.")

            mistakes.append({
                "text": email["text"],
                "your_answer": answer,
                "correct": email["type"],
                "reason": email["reason"]
            })

        print(f"💡 Explanation: {email['reason']}")

    print(f"\n🏅 Final Level: {level}")
    print("\n🎯 Final Score:", score, "/", len(filtered_emails))

    save_score(score, len(filtered_emails))

    if score == len(filtered_emails):
        print("🔥 Excellent! You're phishing-aware!")
    elif score >= len(filtered_emails) // 2:
        print("👍 Good, but stay careful!")
    else:
        print("⚠️ You need more awareness!")

    if mistakes:
        review = input("\n🔍 Do you want to review your mistakes? (y/n): ").lower()
        
        if review == "y":
            print("\n📘 Reviewing Mistakes:\n")
            
            for i, m in enumerate(mistakes, 1):
                print(f"❌ Mistake {i}:")
                print(f"Message: {m['text']}")
                print(f"Your answer: {m['your_answer']}")
                print(f"Correct answer: {m['correct']}")
                print(f"Explanation: {m['reason']}")
                print("-" * 40)
    else:
        print("\n🎉 No mistakes! Perfect run!")

run_simulator()