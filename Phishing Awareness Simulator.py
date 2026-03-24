import random
import json
import os

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

def choose_difficulty():
    print("Select difficulty: easy / medium / hard")
    while True:
        choice = input("👉 ").lower()
        if choice in ["easy", "medium", "hard"]:
            return choice
        print("Invalid choice. Try again.")

def run_simulator():
    print("🔐 Phishing Awareness Simulator 🔐")
    print("Type 'p' for phishing, 'l' for legit\n")

    difficulty = choose_difficulty()
    filtered_emails = [e for e in emails if e["difficulty"] == difficulty]

    score = 0
    lives = 3

    questions = random.sample(filtered_emails, len(filtered_emails))

    for i, email in enumerate(questions):
        if lives == 0:
            print("\n💀 Game Over! You're out of lives.")
            break

        print(f"\n📩 Message {i+1}:")
        print(email["text"])

        answer = input("\nIs this phishing or legit? (p/l): ").lower()

        if (answer == "p" and email["type"] == "phishing") or \
           (answer == "l" and email["type"] == "legit"):
            print("✅ Correct!")
            score += 1
        else:
            print("❌ Wrong!")
            lives -= 1
            print(f"❤️ Lives left: {lives}")

        print(f"💡 Explanation: {email['reason']}")

    print("\n🎯 Final Score:", score, "/", len(filtered_emails))

    save_score(score, len(filtered_emails))

    if score == len(filtered_emails):
        print("🔥 Excellent! You're phishing-aware!")
    elif score >= len(filtered_emails) // 2:
        print("👍 Good, but stay careful!")
    else:
        print("⚠️ You need more awareness!")

run_simulator()