import json
from collections import defaultdict, Counter
import math
from typing import List, Dict, Tuple, Set
from tqdm import tqdm

class WordleSolver:
    def __init__(self, all_words_path: str = "official_wordle_word_list.json",
                 freq_words_path: str = "five_letter_words_order_by_freq.json"):
        self.all_words: List[str] = self._load_words(all_words_path)
        self.freq_order: List[str] = self._load_words(freq_words_path)
        self.freq_dict: Dict[str, int] = {word: idx for idx, word in enumerate(self.freq_order)}

        self.possible_words: Set[str] = set(self.all_words)
        self.guess_history: List[Tuple[str, str]] = []
        self.best_opener = "SALET"

    def _load_words(self, path: str) -> List[str]:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            words = [w.strip().upper() for w in data if len(w.strip()) == 5]
            print(f"Loaded {len(words)} words from {path}")
            return words
        except Exception as e:
            print(f"Error loading {path}: {e}")
            return []

    def normalize_feedback(self, guess: str, feedback: str):
        """
        Apply implicit yellow patch for real wordle feedback
        eg. guess = eieio, feedback = YY---
        output: YYYY-
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
        result = ['-'] * 5

        # Greens
        for i in range(5):
            if guess[i] == secret[i]:
                result[i] = 'G'

        # Yellows
        for i in range(5):
            if result[i] == '-':
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

    def find_best_guess(self) -> Tuple[str, float]:
        """Return best guess by entropy."""
        if len(self.possible_words) <= 1:
            return next(iter(self.possible_words), ""), 0.0

        possible_list = list(self.possible_words)
        candidates = self.all_words  # Adjust for speed vs quality

        best_word, best_entropy = "", -1.0

        for cand in tqdm(candidates):
            ent = self.compute_entropy(cand, possible_list)
            if ent > best_entropy:
                best_entropy = ent
                best_word = cand

        return best_word, best_entropy

    def get_sorted_possible(self) -> List[str]:
        """Possible words sorted by frequency."""
        return sorted(
            self.possible_words,
            key=lambda w: self.freq_dict.get(w, 999999)
        )

    def is_valid_input(self, fb: str):
        fb = fb.upper()
        for letter in fb:
            if letter not in ["G", "Y", "-"]:
                return False
        return True

    def play(self):
        print("=== Wordle Solver (Entropy-based) ===")
        print(f"Recommended first guess: {self.best_opener}\n")

        round_num = 1
        while len(self.possible_words) > 1 and round_num <= 6:
            print(f"\n--- Round {round_num} | {len(self.possible_words)} possible words ---")

            if round_num == 1:
                best_guess = self.best_opener
                print(f"Recommended guess → {self.best_opener}")
            else:
                best_guess, entropy = self.find_best_guess()
                print(f"Recommended guess → {best_guess} (entropy: {entropy:.3f})")

            if len(self.possible_words) <= 15:
                print("Remaining possibilities:", self.get_sorted_possible())

            # User input
            guess = input("\nWhat did you guess? (Enter = recommended): ").strip().upper()
            if not guess:
                guess = best_guess or self.best_opener

            fb = ""
            while len(fb) != 5 or not self.is_valid_input(fb):
                fb = input("Feedback (e.g. YG--G): ").strip().upper()

            fb = self.normalize_feedback(guess, fb)

            self.update_possible_words(guess, fb)
            round_num += 1

        if len(self.possible_words) == 1:
            print(f"\n🎉 The answer is: {next(iter(self.possible_words))}")
        else:
            print("\nRemaining possibilities:", self.get_sorted_possible()[:30])


if __name__ == "__main__":
    solver = WordleSolver()
    solver.play()
    # print(solver.get_feedback("hello", "lmaoo"))
