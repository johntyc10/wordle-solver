import json
from collections import defaultdict
import math
from typing import List, Dict, Tuple, Set
from tqdm import tqdm
from datetime import datetime
from pathlib import Path

LOG_FILE_PATH = "./logs/wordle_solver/" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S.txt")

def log(string: str = ""):
    print(string)
    path = Path(LOG_FILE_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE_PATH, "a") as f:
        f.write(string + "\n")

class WordleSolver:
    def __init__(self, all_words_path: str = "./words/official_wordle_word_list.json",
                 freq_words_path: str = "./words/five_letter_words_order_by_freq.json"):
        self.all_words: List[str] = self._load_words(all_words_path)
        self.freq_order: List[str] = self._load_words(freq_words_path)
        self.freq_dict: Dict[str, int] = {word: idx for idx, word in enumerate(self.freq_order)}

        self.possible_words: Set[str] = set(self.all_words)
        self.guess_history: List[Tuple[str, str]] = []
        self.best_opener = "TARES"

    def _load_words(self, path: str) -> List[str]:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            words = [w.strip().upper() for w in data if len(w.strip()) == 5]
            log(f"Loaded {len(words)} words from {path}")
            return words
        except Exception as e:
            log(f"Error loading {path}: {e}")
            return []

    def normalize_feedback(self, guess: str, feedback: str):
        """
        Apply implicit yellow patch for real wordle feedback
        eg. guess = eieio, feedback = YYBBB
        output: YYYYB
        """
        feedback = feedback.upper()
        result = [letter for letter in feedback]
        for i in range(len(feedback)):
            if feedback[i] == "Y":
                for j in range(i+1, len(guess), 1):
                    if guess[j] == guess[i]:
                        result[j] = "Y"

        return "".join(result)

    def get_feedback(self, guess: str, secret: str) -> str:
        """Correct Wordle feedback (greens first, then yellows)."""
        guess = guess.upper()
        secret = secret.upper()
        result = ['B'] * 5

        # Greens
        for i in range(5):
            if guess[i] == secret[i]:
                result[i] = 'G'

        # Yellows
        for i in range(5):
            if result[i] == 'B':
                letter = guess[i]
                if letter in secret:
                    result[i] = 'Y'

        return ''.join(result)

    def update_possible_words(self, guess: str, feedback: str):
        feedback = feedback.upper()
        self.possible_words = {
            w for w in self.possible_words
            if self.get_feedback(guess, w) == feedback
        }
        self.guess_history.append((guess.upper(), feedback))

    def compute_entropy(self, guess: str, possible: List[str]) -> float:
        """Shannon entropy for a guess."""
        if not possible:
            return 0.0

        pattern_counts: Dict[str, int] = defaultdict(int)
        for secret in possible:
            fb = self.get_feedback(guess, secret)
            pattern_counts[fb] += 1

        total = len(possible)
        entropy = 0.0
        for count in pattern_counts.values():
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)
        return entropy

    def find_best_guesses(self) -> Tuple[str, float]:
        """Return a list of word-entropy tuples sorted by entropy by descending order."""
        if len(self.possible_words) <= 1:
            return next(iter(self.possible_words), ""), 0.0

        possible_list = list(self.possible_words)
        candidates = self.all_words

        word_entropy: List[Tuple[str, int]] = []

        for cand in tqdm(candidates):
            ent = self.compute_entropy(cand, possible_list)
            word_entropy.append((cand, ent))

        sorted_word_entropy = sorted(word_entropy, key=lambda x: x[1], reverse=True)
        return sorted_word_entropy

    def get_sorted_possible(self) -> List[str]:
        """Possible words sorted by frequency."""
        return sorted(
            self.possible_words,
            key=lambda w: self.freq_dict.get(w, 999999)
        )

    def is_valid_input(self, fb: str):
        fb = fb.upper()
        for letter in fb:
            if letter not in ["G", "Y", "B"]:
                return False
        return True

    def is_in_word_list(self, word: str):
        return word in self.all_words

    def play(self, evaluate_entropy_in_first_round=False):
        log("=== Wordle Solver (Entropy-based) ===")
        log(f"Recommended first guess: TARES, SALET, CRANE, etc")

        round_num = 1
        while len(self.possible_words) > 1 and round_num <= 6:
            log(f"\n--- Round {round_num} | {len(self.possible_words)} possible words ---")

            if round_num == 1 and not evaluate_entropy_in_first_round:
                best_guess = self.best_opener
                log("Recommended guess → TARES (entropy: 6.159)")
                log("2th guess → LARES (entropy: 6.115)")
                log("3th guess → RALES (entropy: 6.097)")
                log("4th guess → RATES (entropy: 6.084)")
                log("5th guess → RANES (entropy: 6.077)")
            else:
                log("Evaluating best guesses...")
                word_entropy = self.find_best_guesses()
                log("Done!")
                best_guess = word_entropy[0][0]
                log(f"Recommended guess → {best_guess} (entropy: {word_entropy[0][1]:.3f})")
                for i in range(1, 5):
                    word, entropy = word_entropy[i]
                    log(f"{i+1}th guess → {word} (entropy: {entropy:.3f})")

            if len(self.possible_words) <= 15:
                log("Remaining possibilities:", self.get_sorted_possible())

            log()

            # User input
            guess = "a string which is not in word list and is not empty"
            while guess and not self.is_in_word_list(guess):
                guess = input("What did you guess? (Enter = recommended): ").strip().upper()
            if not guess:
                guess = best_guess

            fb = "a string of which length is not equal to 5 and is not a valid input"
            while len(fb) != 5 or not self.is_valid_input(fb):
                fb = input("Feedback (e.g. YGBBG): ").strip().upper()

            fb = self.normalize_feedback(guess, fb)

            self.update_possible_words(guess, fb)
            round_num += 1

        if len(self.possible_words) == 1:
            log(f"\n🎉 The answer is: {next(iter(self.possible_words))}")
        else:
            log("\nRemaining possibilities:", self.get_sorted_possible()[:30])


if __name__ == "__main__":
    solver = WordleSolver()
    solver.play()
