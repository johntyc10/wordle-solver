import json
from collections import defaultdict
import math
from typing import List, Dict, Tuple, Set, Union
from datetime import datetime
from pathlib import Path

# tqdm fallback
try:
    from tqdm import tqdm
    print("Module tqdm is installed, loading bar will appear.")
except ImportError:
    print("Module tqdm is not detected, loading bar will be gone.")
    def tqdm(iterable, **kwargs):
        return iterable


def get_log_file_path() -> Path:
    """Generate log file path using pathlib."""
    logs_dir = Path("./logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return logs_dir / f"{timestamp}.txt"


LOG_FILE_PATH: Path = get_log_file_path()


def log(*values, sep=" ", end="\n"):
    if not values:
        string = ""
    else:
        string = " ".join([str(i) for i in values])

    print(string, sep=sep, end=end)

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(f"{time_now} | {string}".strip() + end)


class BaseWordle:
    def __init__(self, use_tqdm: bool = True):
        self.all_words_path = Path("./words/nyt-wordle-allowed-guesses-2026-03-06.json")
        self.possible_words_path = Path("./words/wordle-answers-alphabetical.json")
        self.freq_words_path = Path("./words/five_letter_words_order_by_freq.json")

        self.all_words: List[str] = self._load_words(self.all_words_path)
        self.possible_words: Set[str] = set(self._load_words(self.possible_words_path))
        self.freq_order: List[str] = self._load_words(self.freq_words_path)
        self.freq_dict: Dict[str, int] = {word: idx for idx, word in enumerate(self.freq_order)}

        self.guess_history: List[Tuple[str, str]] = []
        self.best_opener = "TARES"

        if use_tqdm:
            self.tqdm = tqdm
        else:
            self.tqdm = lambda iter: iter

    def _load_words(self, path: Path) -> List[str]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            words = [w.strip().upper() for w in data if len(w.strip()) == 5]
            log(f"Loaded {len(words)} words from {path.name}")
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
                for j in range(i + 1, len(guess)):
                    if guess[j] == guess[i]:
                        result[j] = "Y"
        return "".join(result)

    def get_feedback(self, guess: str, secret: str) -> str:
        """Correct Wordle feedback (greens first, then yellows)."""
        guess = guess.upper()
        secret = secret.upper()
        result = ["B"] * 5

        # Greens
        for i in range(5):
            if guess[i] == secret[i]:
                result[i] = "G"

        # Yellows
        secret_count = defaultdict(int)  # keeps track of which letters have been assigned yellow (secret_count[letter] > 0)
        for i in range(5):
            if result[i] != "G":
                secret_count[secret[i]] += 1

        for i in range(5):
            if result[i] == "B":
                letter = guess[i]
                if letter in secret_count and secret_count[letter] > 0:
                    result[i] = "Y"
                    secret_count[letter] -= 1

        return "".join(result)

    def update_possible_words(self, guess: str, feedback: str):
        feedback = feedback.upper()
        self.possible_words = {
            w for w in self.possible_words
            if self.get_feedback(guess, w) == feedback
        }
        self.guess_history.append((guess.upper(), feedback, len(self.possible_words)))

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

    def find_best_guesses(self) -> List[Tuple[str, float]]:
        """Return a list of word-entropy tuples sorted by entropy descending."""
        if len(self.possible_words) <= 1:
            word = next(iter(self.possible_words), "")
            return [(word, 0.0)]

        possible_list = list(self.possible_words)
        candidates = self.all_words

        word_entropy: List[Tuple[str, float]] = []

        for cand in self.tqdm(candidates):
            ent = self.compute_entropy(cand, possible_list)
            word_entropy.append((cand, ent))

        return sorted(word_entropy, key=lambda x: x[1], reverse=True)

    def is_valid_feedback(self, fb: str) -> bool:
        fb = fb.upper()
        return len(fb) == 5 and all(letter in "GYB" for letter in fb)

    def is_in_word_list(self, word: str) -> bool:
        return word in self.all_words


if __name__ == "__main__":
    base = BaseWordle()
    base.compute_entropy(
        
    )
