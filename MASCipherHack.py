import random
import string
from tqdm import trange

CAESAR_OFFSET = 65
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
best_score = float('inf')
# Simulated annealing
INITIAL_PROBABILITY = 0.03
FINAL_PROBABILITY = 0.0001
# Amount of iterations and restart to run
RESTARTS = 25
ITERATIONS_PER_RESTART = 80000

encrypted = input("Input text to decrypt: ").upper()

# Letter-frequency scoring
ENGLISH_FREQ = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7,
    'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0,
}

COMMON_DIGRAMS = [
    "TH", "HE", "IN", "ER", "AN", "RE", "ON", "AT", "EN", "ND", "ED", "AR", "AL", "ET", "ED", "IT"
]

COMMON_TRIGRAMS = [
    "THE", "AND", "FOR", "ING", "ION", "TIO", "ENT", "THA", "HER", "TER", "ERE", "ATE", "HIS", 
]

COMMON_WORDS = [
    "THE", "AND", "TO", "OF", "IN", "IS", "BE", "FOR", "ON", "WITH", "THERE", "THAT", "HAVE", "ANY", "HOW"
]

COMMON_SMALL_WORDS = {
    "THE", "BE", "TO", "OF", "AND", "A", "IN", "THAT", "HAVE", "I", "IT", "FOR", "NOT", "ON", "WITH", "HE", "AS", "YOU", "DO", "AT", "HOW"
}

def create_random_key():
    return ''.join(random.sample(string.ascii_uppercase, 26))

def letter_frequency_score(text):
    if len(text) == 0:
        return float('inf')

    total = len(text)
    score = 0

    for letter, expected in ENGLISH_FREQ.items():
        observed = text.count(letter) / total * 100
        score += abs(observed - expected)

    return score

def swap_two_letters(key):
    key_list = list(key)
    i, j = random.sample(range(26), 2)
    key_list[i], key_list[j] = key_list[j], key_list[i]
    return ''.join(key_list)

# Progress Bar stuff to account for restarts
TOTAL_ITERATIONS = RESTARTS * ITERATIONS_PER_RESTART
loading_bar = trange(TOTAL_ITERATIONS)

top_results = [
    (float('inf'), "", ""),
    (float('inf'), "", ""),
    (float('inf'), "", "")
]

for restart in range(RESTARTS):

    current_key = create_random_key()
    current_score = float('inf')

    for i in range(ITERATIONS_PER_RESTART):
        loading_bar.update(1)

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
        freq_score *= 0.5

        digram_penalty = 0
        for dg in COMMON_DIGRAMS:
            digram_penalty -= plaintext.count(dg)

        trigram_penalty = 0
        for tg in COMMON_TRIGRAMS:
            trigram_penalty -= plaintext.count(tg) * 2

        word_bonus = 0
        words = plaintext.split()
        for w in words:
            if w in COMMON_SMALL_WORDS:
                word_bonus -= 5
            elif len(w) <= 3:
                word_bonus += 2   # penalize short words that arent "words"
            elif 4 <= len(w) <= 7 and w not in COMMON_WORDS:
                word_bonus += 3 # penalize random 4-7 letter words

        candidate_score = freq_score + digram_penalty + trigram_penalty + word_bonus
        # ----------------------

        progress = loading_bar.n / TOTAL_ITERATIONS
        acceptable_prob = INITIAL_PROBABILITY * (1 - progress) + FINAL_PROBABILITY * progress

        if candidate_score < current_score or random.random() < acceptable_prob:
            current_key = candidate_key
            current_score = candidate_score

        if candidate_score < top_results[2][0]:
            top_results[2] = (candidate_score, candidate_key, plaintext)
            top_results.sort(key=lambda x: x[0])

        if i % 100 == 0:
            loading_bar.set_description(
                f"Best score: {top_results[0][0]:.2f}"
            )

loading_bar.close()

print("\nTop 3 Results:")
print("Rank\tScore\t\tKey\t\t\tPlaintext")

for i, (score, key, text) in enumerate(top_results, start=1):
    print(f"{i}\t{score:.2f}\t{key}\t{text}")