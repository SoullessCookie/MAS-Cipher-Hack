import random
import string
from tqdm import trange

CAESAR_OFFSET = 65
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

encrypted = input("Input text to decrypt: ").upper()

best_key = ""
best_score = float('inf')
best_answer = ""

# Letter-frequency scoring
ENGLISH_FREQ = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7,
    'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0,
}

COMMON_DIGRAMS = [
    "TH", "HE", "IN", "ER", "AN", "RE", "ON", "AT", "EN", "ND"
]

COMMON_TRIGRAMS = [
    "THE", "AND", "FOR"
]
COMMON_WORDS = [
    "THE", "AND", "OVER", "FOX", "DOG", "BROWN"
]

def create_random_string():
    return ''.join(random.sample(string.ascii_uppercase, 26))

def letter_frequency_score(text):
    if len(text) == 0:
        return float('inf')

    total = len(text)
    score = 0

    for letter, expected in ENGLISH_FREQ.items():
        observed = text.count(letter) / total * 100
        score += abs(observed - expected)

    return score  # lower = better

def swap_two_letters(key):
    key_list = list(key)
    i, j = random.sample(range(26), 2)
    key_list[i], key_list[j] = key_list[j], key_list[i]
    return ''.join(key_list)

# Initial key generation
current_key = create_random_string()
current_score = float('inf')

# Iterations to run through
loading_bar = trange(500000)

top_results = [
    (float('inf'), "", ""),
    (float('inf'), "", ""),
    (float('inf'), "", "")
]

for i in loading_bar:

    candidate_key = swap_two_letters(current_key)

    plaintext = ""
    text = ""

    for char in encrypted:
        if 'A' <= char <= 'Z':
            position = ord(char) - CAESAR_OFFSET
            decoded_char = candidate_key[position]
            plaintext += decoded_char
            text += decoded_char
        else:
            plaintext += char

    # ---- Scoring Math ----
    freq_score = letter_frequency_score(text)

    digram_penalty = 0
    for dg in COMMON_DIGRAMS:
        digram_penalty -= plaintext.count(dg) * 2

    trigram_penalty = 0
    for tg in COMMON_TRIGRAMS:
        trigram_penalty -= plaintext.count(tg) * 4

    word_bonus = 0
    for word in COMMON_WORDS:
        if word in plaintext:
            word_bonus -= 10

    candidate_score = freq_score + digram_penalty + trigram_penalty + word_bonus
    # ----------------------

    if candidate_score < current_score:
        current_key = candidate_key
        current_score = candidate_score

    # Put score into top 3 if better than the worse
    if candidate_score < top_results[2][0]:
        top_results[2] = (candidate_score, candidate_key, plaintext)
        top_results.sort(key=lambda x: x[0])

    if i % 100 == 0:
        loading_bar.set_description(f"Best score: {top_results[0][0]:.2f}")

loading_bar.close()

print("\nTop 3 Results:")
print("Rank\tScore\t\tKey\t\t\tPlaintext")

for i, (score, key, text) in enumerate(top_results, start=1):
    print(f"{i}\t{score:.2f}\t{key}\t{text}")