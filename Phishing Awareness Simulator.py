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

# ---------------- DAILY CHALLENGE ----------------

def get_today_date():
    return time.strftime("%Y-%m-%d")

def load_daily_data():
    if os.path.exists("daily.json"):
        with open("daily.json", "r") as f:
            return json.load(f)
    return {}

def save_daily_data(data):
    with open("daily.json", "w") as f:
        json.dump(data, f, indent=4)

def daily_challenge():
    data = load_daily_data()
    today = get_today_date()

    if data.get("last_played") == today:
        print("📅 You already completed today's challenge. Come back tomorrow!")
        return

    print("\n🔥 DAILY CHALLENGE MODE 🔥")
    print("🎯 Bonus XP enabled!")

    questions = random.sample(emails, min(3, len(emails)))

    score = 0
    xp = 0

    for i, email in enumerate(questions, 1):
        print(f"\n📩 Challenge {i}:")
        print(email["text"])

        answer = input("Phishing or legit? (p/l): ").lower()

        if (
            (answer == "p" and email["type"] == "phishing") or
            (answer == "l" and email["type"] == "legit")
        ):
            print("✅ Correct!")
            score += 1
            xp += 5
        else:
            print("❌ Wrong!")

        print(f"💡 {email['reason']}")

    print(f"\n🏆 Daily Score: {score}/{len(questions)}")
    print(f"✨ Bonus XP Earned: {xp}")

    data["last_played"] = today
    save_daily_data(data)

# ---------------- NORMAL SYSTEM ----------------

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

def update_rank(xp):
    if xp >= 15:
        return "🧠 Expert"
    elif xp >= 10:
        return "💻 Advanced"
    elif xp >= 5:
        return "🔐 Intermediate"
    else:
        return "🟢 Beginner"

def get_adaptive_pool(performance):
    if performance >= 0.8:
        pool = [e for e in emails if e["difficulty"] == "hard"]
    elif performance >= 0.5:
        pool = [e for e in emails if e["difficulty"] in ["medium", "hard"]]
    else:
        pool = [e for e in emails if e["difficulty"] in ["easy", "medium"]]
    return pool

def get_streak_multiplier(streak):
    if streak >= 5:
        return 2
    return 1

def run_simulator():
    print("🔐 Phishing Awareness Simulator 🔐")
    show_high_scores()

    print("\nChoose mode:")
    print("1. Normal Mode")
    print("2. Daily Challenge")

    mode = input("👉 ").strip()

    if mode == "2":
        daily_challenge()
        return

    print("Type 'p' for phishing, 'l' for legit\n")

    difficulty = choose_difficulty()
    filtered_emails = [e for e in emails if e["difficulty"] == difficulty]

    score = 0
    lives = 3
    streak = 0
    level = 1
    power_ups = 0
    xp = 0
    rank = "🟢 Beginner"
    skipped = 0
    mistakes = []

    for i in range(len(filtered_emails)):

        if lives == 0:
            print("\n💀 Game Over!")
            break

        performance = score / i if i > 0 else 0
        questions_pool = get_adaptive_pool(performance)
        email = random.choice(questions_pool)

        time_limit = 8

        print(f"\n📩 Message {i+1} (Level {level}):")
        print(email["text"])
        print(f"\n⏳ You have {time_limit} seconds!")

        if power_ups > 0:
            print(f"\n⚡ Power-Ups: {power_ups}")
            use = input("Use power-up? (y/n): ").lower()

            if use == "y":
                print("1. +3 seconds\n2. +1 life\n3. Show hint\n4. Skip")
                choice = input("Choose: ")

                if choice == "1":
                    time_limit += 3
                elif choice == "2":
                    lives += 1
                elif choice == "3":
                    print(f"💡 {email['reason']}")
                elif choice == "4":
                    power_ups -= 1
                    skipped += 1
                    continue

                power_ups -= 1

        start = time.time()
        answer = input("Phishing or legit? (p/l): ").lower()
        end = time.time()

        if end - start > time_limit:
            answer = "timeout"
            print("⏰ Time's up!")

        if answer != "timeout" and (
            (answer == "p" and email["type"] == "phishing") or
            (answer == "l" and email["type"] == "legit")
        ):
            multiplier = get_streak_multiplier(streak)
            gained_xp = 2 * multiplier

            print("✅ Correct!")
            score += 1
            streak += 1
            xp += gained_xp
            rank = update_rank(xp)

            print(f"✨ XP: {xp} (+{gained_xp}) | Rank: {rank}")

            if streak % 2 == 0:
                power_ups += 1
                print("⚡ Power-Up earned!")

            if streak % 3 == 0:
                level += 1
                print(f"🚀 Level {level}!")

        else:
            lives -= 1
            streak = 0
            print("❌ Wrong!")
            print(f"❤️ Lives: {lives}")

            mistakes.append({
                "text": email["text"],
                "your_answer": answer,
                "correct": email["type"],
                "reason": email["reason"]
            })

        print(f"💡 {email['reason']}")

    print(f"\n🏆 Score: {score}/{len(filtered_emails)}")
    print(f"🏅 Rank: {rank} | XP: {xp}")

    save_score(score, len(filtered_emails))

    if mistakes:
        review = input("\nReview mistakes? (y/n): ").lower()
        if review == "y":
            for m in mistakes:
                print("\n---")
                print(m["text"])
                print("You:", m["your_answer"])
                print("Correct:", m["correct"])
                print("Why:", m["reason"])

run_simulator()