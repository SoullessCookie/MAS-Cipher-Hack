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
loading_bar = trange(100000)

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

    candidate_score = letter_frequency_score(text)

    if candidate_score < current_score:
        current_key = candidate_key
        current_score = candidate_score

        # Update global best
        if candidate_score < best_score:
            best_score = candidate_score
            best_key = candidate_key
            best_answer = plaintext
    
    if i % 100 == 0:
        loading_bar.set_description(f"Best score: {best_score:.2f}")

loading_bar.close()
print("Key\t\t\t\tScore\t\t\tPlaintext")
print(f"{best_key}\t{best_score}\t{best_answer}")