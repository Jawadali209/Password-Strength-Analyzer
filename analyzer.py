import math
import string
from collections import Counter

from config import (
    MIN_LENGTH, RECOMMENDED_LENGTH,
    SCORE, PENALTY, STRENGTH, DICTIONARY_FILE, GUESS_RATE,
)


# Load common words from the dictionary file
def load_dictionary(file_path=DICTIONARY_FILE):
    words = set()
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                word = line.strip().lower()
                if word:
                    words.add(word)
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. Dictionary check disabled.")
    return words


DICTIONARY_WORDS = load_dictionary()


def check_password_length(password):
    return len(password)


# Which character classes are present
def check_character_types(password):
    return {
        "Uppercase": any(c.isupper() for c in password),
        "Lowercase": any(c.islower() for c in password),
        "Digit": any(c.isdigit() for c in password),
        "Symbol": any(not c.isalnum() for c in password),
    }


# Dictionary words of length 3+ found inside the password
def check_dictionary_words(password):
    password = password.lower()
    found = [w for w in DICTIONARY_WORDS if len(w) >= 3 and w in password]
    return sorted(found)


# Common keyboard walks and very common strings
def check_keyboard_patterns(password):
    password = password.lower()
    patterns = [
        "qwerty", "asdf", "zxcv", "qazwsx", "wasd",
        "12345", "123456", "987654", "1234", "password", "admin",
    ]
    return [p for p in patterns if p in password]


# Ascending or descending numeric runs like 123 or 654
def check_sequential_numbers(password):
    found = []
    for i in range(len(password) - 2):
        part = password[i:i + 3]
        if part.isdigit():
            if ord(part[1]) == ord(part[0]) + 1 and ord(part[2]) == ord(part[1]) + 1:
                found.append(part)
            elif ord(part[1]) == ord(part[0]) - 1 and ord(part[2]) == ord(part[1]) - 1:
                found.append(part)
    return sorted(set(found))


# Characters that appear 3 or more times
def check_repeated_characters(password):
    counts = Counter(password)
    return [(char, count) for char, count in counts.items() if count >= 3]


# Predictable letter-digit alternation like a1b2c3
def check_alternating_pattern(password):
    if len(password) < 6:
        return False
    matches = 0
    for i in range(len(password) - 1):
        a, b = password[i], password[i + 1]
        if (a.isalpha() and b.isdigit()) or (a.isdigit() and b.isalpha()):
            matches += 1
    return matches >= len(password) // 2


def get_password_statistics(password):
    return {
        "Length": len(password),
        "Uppercase Letters": sum(c.isupper() for c in password),
        "Lowercase Letters": sum(c.islower() for c in password),
        "Digits": sum(c.isdigit() for c in password),
        "Special Characters": sum(not c.isalnum() for c in password),
        "Unique Characters": len(set(password)),
    }


# Theoretical entropy in bits
def calculate_entropy(password):
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(c in string.punctuation for c in password):
        pool += len(string.punctuation)
    if pool == 0:
        return 0.0, 0
    entropy = round(len(password) * math.log2(pool), 2)
    return entropy, pool


# Entropy reduced for predictable patterns
def calculate_effective_entropy(password):
    entropy, _ = calculate_entropy(password)
    effective = entropy

    if len(password) < MIN_LENGTH:
        effective -= 35
    elif len(password) < 12:
        effective -= 20
    elif len(password) < RECOMMENDED_LENGTH:
        effective -= 10

    if check_dictionary_words(password):
        effective -= min(len(check_dictionary_words(password)) * 20, 40)
    if check_keyboard_patterns(password):
        effective -= 15
    if check_sequential_numbers(password):
        effective -= 15
    if check_repeated_characters(password):
        effective -= 10
    if check_alternating_pattern(password):
        effective -= 15

    return max(0.0, round(effective, 2))


# Final score from 0 to 100 with a list of weaknesses
def calculate_password_score(password):
    score = 0
    weaknesses = []
    length = len(password)

    if length >= RECOMMENDED_LENGTH:
        score += SCORE["LENGTH_15"]
    elif length >= 12:
        score += SCORE["LENGTH_12"]
    elif length >= MIN_LENGTH:
        score += SCORE["LENGTH_8"]
        weaknesses.append(
            f"Password length can be improved (recommended: {RECOMMENDED_LENGTH}+ characters)"
        )
    else:
        weaknesses.append(
            f"Password is too short (minimum recommended: {MIN_LENGTH} characters)"
        )

    char_types = check_character_types(password)
    for key, label in [
        ("Uppercase", "uppercase letter"),
        ("Lowercase", "lowercase letter"),
        ("Digit", "digit"),
        ("Symbol", "special character"),
    ]:
        if char_types[key]:
            score += SCORE[key.upper()]
        else:
            weaknesses.append(f"Missing {label}")

    effective = calculate_effective_entropy(password)
    if effective >= 60:
        score += SCORE["ENTROPY_HIGH"]
    elif effective >= 40:
        score += SCORE["ENTROPY_MEDIUM"]
    elif effective >= 25:
        score += SCORE["ENTROPY_LOW"]

    words = check_dictionary_words(password)
    if words:
        score -= PENALTY["DICTIONARY"]
        weaknesses.append("Contains dictionary word(s): " + ", ".join(words))

    patterns = check_keyboard_patterns(password)
    if patterns:
        score -= PENALTY["KEYBOARD"]
        weaknesses.append("Contains keyboard pattern(s): " + ", ".join(patterns))

    sequences = check_sequential_numbers(password)
    if sequences:
        score -= PENALTY["SEQUENTIAL"]
        weaknesses.append("Contains sequential number(s): " + ", ".join(sequences))

    if check_repeated_characters(password):
        score -= PENALTY["REPEATED"]
        weaknesses.append("Contains repeated characters")

    if check_alternating_pattern(password):
        score -= PENALTY["PATTERN"]
        weaknesses.append("Contains predictable letter-number pattern")

    score = max(0, min(score, 100))
    return score, weaknesses


def get_strength_level(score):
    if score <= STRENGTH["VERY_WEAK"]:
        return "Very Weak"
    elif score <= STRENGTH["WEAK"]:
        return "Weak"
    elif score <= STRENGTH["MODERATE"]:
        return "Moderate"
    elif score <= STRENGTH["STRONG"]:
        return "Strong"
    return "Excellent"


def generate_recommendations(password):
    recommendations = []
    if len(password) < RECOMMENDED_LENGTH:
        recommendations.append(
            f"Increase password length to at least {RECOMMENDED_LENGTH} characters."
        )
    if check_dictionary_words(password):
        recommendations.append("Avoid using common dictionary words.")
    if check_keyboard_patterns(password):
        recommendations.append("Avoid keyboard patterns such as qwerty or asdf.")
    if check_sequential_numbers(password):
        recommendations.append("Avoid sequential numbers such as 123 or 456.")
    if check_repeated_characters(password):
        recommendations.append("Avoid repeating the same character multiple times.")
    if check_alternating_pattern(password):
        recommendations.append("Avoid predictable letter-number combinations.")
    if not all(check_character_types(password).values()):
        recommendations.append(
            "Use a mix of uppercase, lowercase, digits and special characters."
        )
    if not recommendations:
        recommendations.append("Excellent password. No improvements needed.")
    return recommendations


def identify_attack(password):
    if check_dictionary_words(password):
        return "Dictionary Attack"
    elif check_keyboard_patterns(password):
        return "Keyboard Pattern Attack"
    elif check_sequential_numbers(password):
        return "Sequential Attack"
    elif check_alternating_pattern(password) or check_repeated_characters(password):
        return "Pattern Attack"
    return "Brute Force Attack"


# Convert seconds into standard cyber-security crack-time wording
def humanise_time(seconds):
    if seconds < 1:
        return "Instantly"
    minute, hour, day = 60, 3600, 86400
    month, year, century = 2_592_000, 31_536_000, 3_153_600_000

    for limit, size, unit in [
        (minute, 1, "second"),
        (hour, minute, "minute"),
        (day, hour, "hour"),
        (month, day, "day"),
        (year, month, "month"),
        (century, year, "year"),
    ]:
        if seconds < limit:
            value = round(seconds / size)
            return f"{value} {unit}" if value == 1 else f"{value} {unit}s"
    return "Centuries"


# Realistic crack time from effective entropy (average = 2^(bits-1) guesses)
def estimate_realistic_crack_time(password):
    effective = calculate_effective_entropy(password)
    if effective <= 0:
        return "Instantly"
    bits = min(effective, 200)
    seconds = (2 ** (bits - 1)) / GUESS_RATE
    return humanise_time(seconds)


# Full report for one password
def analyze_password(password):
    score, weaknesses = calculate_password_score(password)
    entropy, pool = calculate_entropy(password)
    return {
        "Password": password,
        "Score": score,
        "Strength": get_strength_level(score),
        "Entropy": entropy,
        "Effective Entropy": calculate_effective_entropy(password),
        "Character Pool": pool,
        "Attack Type": identify_attack(password),
        "Estimated Crack Time": estimate_realistic_crack_time(password),
        "Statistics": get_password_statistics(password),
        "Weaknesses": weaknesses,
        "Recommendations": generate_recommendations(password),
    }


if __name__ == "__main__":
    pwd = input("Enter Password: ")
    report = analyze_password(pwd)

    print("\n" + "=" * 55)
    print("PASSWORD ANALYSIS REPORT")
    print("=" * 55)
    print(f"Password             : {report['Password']}")
    print(f"Score                : {report['Score']}/100")
    print(f"Strength             : {report['Strength']}")
    print(f"Entropy              : {report['Entropy']} bits")
    print(f"Effective Entropy    : {report['Effective Entropy']} bits")
    print(f"Attack Type          : {report['Attack Type']}")
    print(f"Estimated Crack Time : {report['Estimated Crack Time']}")

    print("\nWeaknesses")
    print("-" * 55)
    for item in report["Weaknesses"] or ["None"]:
        print(f"- {item}")

    print("\nRecommendations")
    print("-" * 55)
    for item in report["Recommendations"]:
        print(f"- {item}")
    print("=" * 55)
