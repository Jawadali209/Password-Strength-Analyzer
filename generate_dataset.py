import csv
import random
import string

from analyzer import analyze_password
from config import DATASET_FILE

random.seed(42)


def expected_band(category):
    return {
        "Common Password": "Very Weak",
        "Dictionary Password": "Weak",
        "Pattern Password": "Weak",
        "Moderate Password": "Moderate",
        "Strong Password": "Strong",
        "Excellent Random": "Excellent",
    }[category]


rows = []

# Common weak passwords
common = [
    "123456", "password", "12345678", "qwerty", "123456789", "12345",
    "1234", "111111", "000000", "abc123", "letmein", "admin", "welcome",
    "monkey", "login", "iloveyou", "dragon", "sunshine", "princess",
    "football", "master", "hello", "qwerty123", "1q2w3e4r", "aaaaaa",
]
for p in common:
    rows.append((p, "Common Password"))

# Dictionary-based passwords
dict_words = ["computer", "internet", "security", "python", "pakistan",
              "github", "google", "cricket", "student", "manager",
              "database", "network", "software", "welcome", "dragon"]
for w in dict_words:
    rows.append((w + str(random.randint(1, 999)), "Dictionary Password"))
    rows.append((w.capitalize() + "@" + str(random.randint(1, 99)), "Dictionary Password"))
    rows.append((w + "123", "Dictionary Password"))

# Keyboard, sequential, repeated and alternating patterns
patterns = ["asdf1234", "zxcvbnm1", "qazwsx12", "147258369", "987654321",
            "aaa11122", "abcabcabc", "a1b2c3d4", "1212121212", "password123"]
for p in patterns:
    rows.append((p, "Pattern Password"))

# Moderate passwords
def moderate():
    word = random.choice(dict_words).capitalize()
    return word + random.choice(["@", "#", "!", "$"]) + str(random.randint(10, 99))
for _ in range(45):
    rows.append((moderate(), "Moderate Password"))

# Strong random passwords
def strong(length):
    pool = string.ascii_letters + string.digits + "@#!$%&*?"
    return "".join(random.choice(pool) for _ in range(length))
for _ in range(45):
    rows.append((strong(random.randint(11, 13)), "Strong Password"))

# Excellent random passwords
for _ in range(45):
    rows.append((strong(random.randint(16, 24)), "Excellent Random"))

# Analyse every password and write the dataset
with open(DATASET_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "ID", "Password", "Expected Strength", "Actual Strength", "Score",
        "Entropy", "Effective Entropy", "Attack Type",
        "Estimated Crack Time", "Category",
    ])
    for i, (pwd, category) in enumerate(rows, start=1):
        r = analyze_password(pwd)
        writer.writerow([
            i, pwd, expected_band(category), r["Strength"], r["Score"],
            r["Entropy"], r["Effective Entropy"], r["Attack Type"],
            r["Estimated Crack Time"], category,
        ])

print(f"Wrote {len(rows)} passwords to {DATASET_FILE}")
