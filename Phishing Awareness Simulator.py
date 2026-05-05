import random
import json
import os
import time

emails = [
    {"text": "Your bank account has been locked! Click here to verify: http://secure-bank-login.xyz", "type": "phishing", "reason": "Suspicious link and urgent message.", "difficulty": "easy"},
    {"text": "Hi Yassine, your Amazon order has been shipped. Track here: https://amazon.com/orders", "type": "legit", "reason": "Trusted domain and no urgency tricks.", "difficulty": "easy"},
    {"text": "You've won a free iPhone! Claim now: http://free-iphone-win.net", "type": "phishing", "reason": "Too good to be true + fake link.", "difficulty": "medium"},
    {"text": "Reminder: Your university class starts at 10 AM tomorrow.", "type": "legit", "reason": "Normal message, no suspicious links.", "difficulty": "easy"},
    {"text": "Unusual login detected! Reset your password immediately: http://secure-reset-password.co", "type": "phishing", "reason": "Fake domain + urgency.", "difficulty": "medium"},
    {"text": "Dear user, we noticed unusual billing activity. Please login via https://billing-secure-paypal.com to confirm.", "type": "phishing", "reason": "Looks real but domain is fake.", "difficulty": "hard"}
]

def get_today_date():
    return time.strftime("%Y-%m-%d")

def load_json(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def daily_challenge(username):
    data = load_json("daily.json")
    today = get_today_date()

    if data.get(username) == today:
        print("You already completed today's challenge")
        return

    print("Daily Challenge Mode")

    questions = random.sample(emails, min(3, len(emails)))
    score = 0
    xp = 0

    for i, email in enumerate(questions, 1):
        print(f"\nChallenge {i}:")
        print(email["text"])
        answer = input("Phishing or legit? (p/l): ").lower()

        if (answer == "p" and email["type"] == "phishing") or (answer == "l" and email["type"] == "legit"):
            print("Correct")
            score += 1
            xp += 5
        else:
            print("Wrong")

        print(email["reason"])

    print(f"\nScore: {score}/{len(questions)}")
    print(f"XP: {xp}")

    data[username] = today
    save_json("daily.json", data)

def save_score(username, score, total):
    scores = load_json("scores.json")
    if not isinstance(scores, list):
        scores = []

    scores.append({"user": username, "score": score, "total": total})
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]

    save_json("scores.json", scores)

def show_high_scores():
    scores = load_json("scores.json")
    if isinstance(scores, list) and scores:
        print("\nLeaderboard:")
        for s in scores:
            print(f"{s['user']}: {s['score']}/{s['total']}")
    else:
        print("\nNo scores yet")

def choose_difficulty():
    while True:
        choice = input("Select difficulty (easy/medium/hard): ").lower()
        if choice in ["easy", "medium", "hard"]:
            return choice

def update_rank(xp):
    if xp >= 15:
        return "Expert"
    elif xp >= 10:
        return "Advanced"
    elif xp >= 5:
        return "Intermediate"
    else:
        return "Beginner"

def get_adaptive_pool(performance):
    if performance >= 0.8:
        return [e for e in emails if e["difficulty"] == "hard"]
    elif performance >= 0.5:
        return [e for e in emails if e["difficulty"] in ["medium", "hard"]]
    return [e for e in emails if e["difficulty"] in ["easy", "medium"]]

def get_streak_multiplier(streak):
    return 2 if streak >= 5 else 1

def run_simulator():
    print("Phishing Awareness Simulator")

    username = input("Enter your username: ").strip()
    show_high_scores()

    print("\n1. Normal Mode")
    print("2. Daily Challenge")

    mode = input("Choose mode: ").strip()

    if mode == "2":
        daily_challenge(username)
        return

    difficulty = choose_difficulty()
    filtered_emails = [e for e in emails if e["difficulty"] == difficulty]

    score = 0
    lives = 3
    streak = 0
    level = 1
    power_ups = 0
    xp = 0
    rank = "Beginner"
    mistakes = []

    for i in range(len(filtered_emails)):
        if lives == 0:
            print("\nGame Over")
            break

        performance = score / i if i > 0 else 0
        email = random.choice(get_adaptive_pool(performance))

        time_limit = 8

        print(f"\nMessage {i+1} Level {level}")
        print(email["text"])
        print(f"Time limit: {time_limit}s")

        if power_ups > 0:
            use = input("Use power-up? (y/n): ").lower()
            if use == "y":
                print("1. +3 seconds\n2. +1 life\n3. Hint\n4. Skip")
                choice = input("Choose: ")
                if choice == "1":
                    time_limit += 3
                elif choice == "2":
                    lives += 1
                elif choice == "3":
                    print(email["reason"])
                elif choice == "4":
                    power_ups -= 1
                    continue
                power_ups -= 1

        start = time.time()
        answer = input("Phishing or legit? (p/l): ").lower()
        end = time.time()

        if end - start > time_limit:
            answer = "timeout"
            print("Time up")

        if answer != "timeout" and ((answer == "p" and email["type"] == "phishing") or (answer == "l" and email["type"] == "legit")):
            multiplier = get_streak_multiplier(streak)
            gained_xp = 2 * multiplier

            print("Correct")
            score += 1
            streak += 1
            xp += gained_xp
            rank = update_rank(xp)

            if streak % 2 == 0:
                power_ups += 1

            if streak % 3 == 0:
                level += 1
        else:
            lives -= 1
            streak = 0
            print("Wrong")
            print(f"Lives: {lives}")

            mistakes.append({
                "text": email["text"],
                "your_answer": answer,
                "correct": email["type"],
                "reason": email["reason"]
            })

        print(email["reason"])

    print(f"\nFinal Score: {score}/{len(filtered_emails)}")
    print(f"Rank: {rank} XP: {xp}")

    save_score(username, score, len(filtered_emails))

    if mistakes:
        review = input("Review mistakes? (y/n): ").lower()
        if review == "y":
            for m in mistakes:
                print("\n---")
                print(m["text"])
                print("You:", m["your_answer"])
                print("Correct:", m["correct"])
                print("Why:", m["reason"])

run_simulator()