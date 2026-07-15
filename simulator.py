import string

from config import GUESS_RATE
from analyzer import (
    load_dictionary, calculate_entropy, check_character_types, humanise_time,
    calculate_effective_entropy, estimate_realistic_crack_time, identify_attack,
)

WORDLIST = load_dictionary()

_LEET = str.maketrans({"a": "@", "s": "$", "o": "0", "i": "1", "e": "3"})
_COMMON_SUFFIXES = ["", "1", "12", "123", "1234", "!", "@", "123!", "2024", "2025", "01"]


# Try dictionary words plus common human mutations
def dictionary_attack_simulation(password):
    guesses = 0
    for word in sorted(WORDLIST):
        for suffix in _COMMON_SUFFIXES:
            for variant in (
                word + suffix,
                word.capitalize() + suffix,
                word.upper() + suffix,
                (word + suffix).translate(_LEET),
                word.capitalize().translate(_LEET) + suffix,
            ):
                guesses += 1
                if variant == password:
                    return {
                        "strategy": "Dictionary Attack",
                        "cracked": True,
                        "guesses": guesses,
                        "time_seconds": guesses / GUESS_RATE,
                        "time_label": humanise_time(guesses / GUESS_RATE),
                        "note": f"Matched mutation of dictionary word '{word}'.",
                    }
    return {
        "strategy": "Dictionary Attack",
        "cracked": False,
        "guesses": guesses,
        "time_seconds": guesses / GUESS_RATE,
        "time_label": humanise_time(guesses / GUESS_RATE),
        "note": "Not found in dictionary + common-mutation space.",
    }


# Estimate brute-force effort from the character space
def brute_force_simulation(password):
    pool = 0
    types = check_character_types(password)
    if types["Lowercase"]:
        pool += 26
    if types["Uppercase"]:
        pool += 26
    if types["Digit"]:
        pool += 10
    if types["Symbol"]:
        pool += len(string.punctuation)
    pool = max(pool, 1)

    length = max(len(password), 1)
    search_space = pool ** length

    # Realistic time uses effective entropy (accounts for detected patterns),
    # so it stays consistent with the Analyzer tab.
    return {
        "strategy": "Brute Force Attack",
        "character_pool": pool,
        "search_space": search_space,
        "effective_entropy": calculate_effective_entropy(password),
        "time_label": estimate_realistic_crack_time(password),
    }


# Run both strategies and report the fastest one
def simulate_cracking(password):
    dictionary = dictionary_attack_simulation(password)
    brute = brute_force_simulation(password)
    entropy, _ = calculate_entropy(password)

    if dictionary["cracked"]:
        fastest_time = dictionary["time_label"]
    else:
        fastest_time = brute["time_label"]

    return {
        "password": password,
        "entropy_bits": entropy,
        "dictionary": dictionary,
        "brute_force": brute,
        "attack_type": identify_attack(password),
        "estimated_time": fastest_time,
    }


if __name__ == "__main__":
    for demo in ["password", "Welcome123", "P@ssw0rd", "g7#Lq!2vXm9$Rt"]:
        result = simulate_cracking(demo)
        print("=" * 55)
        print(f"Password        : {demo}")
        print(f"Entropy         : {result['entropy_bits']} bits")
        print(f"Dictionary      : cracked={result['dictionary']['cracked']} "
              f"in {result['dictionary']['guesses']} guesses "
              f"({result['dictionary']['time_label']})")
        print(f"Brute force     : {result['brute_force']['time_label']} "
              f"(pool={result['brute_force']['character_pool']})")
        print(f"Attack type     : {result['attack_type']} -> {result['estimated_time']}")
    print("=" * 55)
