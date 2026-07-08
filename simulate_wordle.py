import json
from collections import defaultdict, Counter
import math
from typing import List, Dict, Tuple, Set, Iterable
from tqdm import tqdm
import random

def avg(x: Iterable):
    if len(x) == 0:
        return 0
    return sum(x) / len(x)

class WordleSimulator:
    def __init__(self, all_words_path: str = "official_wordle_word_list.json",
                 freq_words_path: str = "five_letter_words_order_by_freq.json"):
        self.all_words: List[str] = self._load_words(all_words_path)
        self.freq_order: List[str] = self._load_words(freq_words_path)
        self.freq_dict: Dict[str, int] = {word: idx for idx, word in enumerate(self.freq_order)}

        self.best_opener = "TARES"

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

    def find_best_guesses(self) -> Tuple[str, float]:
        """Return a list of word-entropy tuples sorted by entropy by descending order."""
        if len(self.possible_words) <= 1:
            return next(iter(self.possible_words), ""), 0.0

        possible_list = list(self.possible_words)
        candidates = self.all_words

        word_entropy: List[Tuple[str, int]] = []

        for cand in candidates:
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
            if letter not in ["G", "Y", "-"]:
                return False
        return True

    def is_in_word_list(self, word: str):
        return word in self.all_words

    def play_one_game(self, secret: str):
        """
        Simulates playing one game of wordle using optimal approach.
        secret: wordle answer
        """
        round_num = 1
        while round_num <= 6:
            if round_num == 1:
                best_guess = self.best_opener
            else:
                word_entropy = self.find_best_guesses()
                best_guess = word_entropy[0][0]

            # Simulate user input
            guess = best_guess

            fb = self.get_feedback(guess, secret)

            self.update_possible_words(guess, fb)
            if len(self.possible_words) == 1:
                break

            round_num += 1

        if len(self.possible_words) == 1:
            print(f"Answer found after {round_num} rounds. The answer is {next(iter(self.possible_words))}")
        else:
            print(f"Answer not found after 6 rounds. The answer is {secret}")

        return round_num

    def simulate(self, n=100):
        print("=====SIMULATION START=====")
        print("Press ctrl+c to terminate")
        try:
            guesses_taken = []
            games_played = 0
            for i in range(n):
                print(f"GAME {i}/{n}")

                self.possible_words: Set[str] = set(self.all_words)
                self.guess_history: List[Tuple[str, str]] = []

                secret = random.choice(self.all_words)
                guesses = self.play_one_game(secret)
                if guesses <= 6:
                    guesses_taken.append(guesses)
                games_played += 1
        except KeyboardInterrupt:
            pass  # intended way of terminating
        finally:
            print()
            print("=====STATISTICS REPORT=====")
            print(f"First opener used: {self.best_opener}")
            print("Guesses taken distribution:")
            for i in range(1, 7):
                print(f"{i}: {guesses_taken.count(i)}")

            print(f"Average guesses taken: {avg(guesses_taken):.3f}")
            print(f"Success rate: {len(guesses_taken) / games_played * 100:.3f}%")

if __name__ == "__main__":
    sim = WordleSimulator()
    sim.simulate(n=100)
