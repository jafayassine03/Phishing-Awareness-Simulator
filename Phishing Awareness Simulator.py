import random

emails = [
    {
        "text": "Your bank account has been locked! Click here to verify: http://secure-bank-login.xyz",
        "type": "phishing",
        "reason": "Suspicious link and urgent message."
    },
    {
        "text": "Hi Yassine, your Amazon order has been shipped. Track here: https://amazon.com/orders",
        "type": "legit",
        "reason": "Trusted domain and no urgency tricks."
    },
    {
        "text": "You've won a free iPhone! Claim now: http://free-iphone-win.net",
        "type": "phishing",
        "reason": "Too good to be true + fake link."
    },
    {
        "text": "Reminder: Your university class starts at 10 AM tomorrow.",
        "type": "legit",
        "reason": "Normal message, no suspicious links."
    },
    {
        "text": "Unusual login detected! Reset your password immediately: http://secure-reset-password.co",
        "type": "phishing",
        "reason": "Fake domain + urgency."
    }
]

def run_simulator():
    print("🔐 Phishing Awareness Simulator 🔐")
    print("Type 'p' for phishing, 'l' for legit\n")

    score = 0
    questions = random.sample(emails, len(emails))

    for i, email in enumerate(questions):
        print(f"\n📩 Message {i+1}:")
        print(email["text"])

        answer = input("\nIs this phishing or legit? (p/l): ").lower()

        if (answer == "p" and email["type"] == "phishing") or \
           (answer == "l" and email["type"] == "legit"):
            print("✅ Correct!")
            score += 1
        else:
            print("❌ Wrong!")
        
        print(f"💡 Explanation: {email['reason']}")

    print("\n🎯 Final Score:", score, "/", len(emails))

    if score == len(emails):
        print("🔥 Excellent! You're phishing-aware!")
    elif score >= 3:
        print("👍 Good, but stay careful!")
    else:
        print("⚠️ You need more awareness!")

run_simulator()