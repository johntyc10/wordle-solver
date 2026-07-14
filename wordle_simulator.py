from typing import List, Dict, Tuple, Set, Iterable
import random
import time
import copy
from wordle_solver import BaseWordle, log
from datetime import datetime
from pathlib import Path
import json

def avg(x: Iterable):
    if len(x) == 0:
        return 0
    return sum(x) / len(x)

class WordleSimulator(BaseWordle):
    def __init__(self, use_tqdm = False):
        super().__init__(use_tqdm)

        self.all_words_persistence: List[str] = self._load_words(self.all_words_path)
        self.possible_words_persistence: Set[str] = set(self._load_words(self.possible_words_path))

    def reset(self):
        self.all_words = copy.deepcopy(self.all_words_persistence)
        self.possible_words = copy.deepcopy(self.possible_words_persistence)
        self.guess_history: List[Tuple[str, str]] = []
        # log(f"{len(self.all_words) = }")
        # log(f"{len(self.possible_words) = }")

    def save_guess_histories(self):
        filename = f"simulator_guess_histories_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.json"
        dir = Path("./output/")
        dir.mkdir(parents=True, exist_ok=True)

        with open(dir / filename, "w") as f:
            json.dump(self.guess_histories, f, indent=4)

    def print_statistics(self):
        log()
        log("===== STATISTICS REPORT =====")
        log(f"First opener used: {self.first_opener}")

        guesses_taken = [len(hist) for hist in self.guess_histories]
        log("Guesses taken distribution:")
        for i in range(1, 7):
            log(f"{i}: {guesses_taken.count(i)}")

        log(f"Average guesses taken: {avg(guesses_taken):.3f}")
        log(f"Average time taken per game: {avg(self.time_taken):.3f}s")
        log(f"Average time taken per round: {sum(self.time_taken) / sum(guesses_taken):.3f}s")
        log(f"Success rate: {len(guesses_taken) / self.games_played * 100:.3f}% ({len(guesses_taken)}/{self.games_played})")  # couldnt care less about ZeroDivisionError here

    def play_one_game(self, secret: str):
        """
        Simulates playing one game of wordle using optimal approach.
        secret: wordle answer
        """
        finished_rounds = 0
        while finished_rounds < 6:
            log(f"  => Playing round {finished_rounds + 1}")

            if finished_rounds == 0:
                best_guess = self.first_opener
            else:
                word_entropy = self.find_best_guesses()
                best_guess = word_entropy[0][0]

            # Simulate user input
            guess = best_guess

            fb = self.get_feedback(guess, secret)

            self.update_possible_words(guess, fb)
            finished_rounds += 1

            if len(self.possible_words) == 1:
                finished_rounds += 1
                self.guess_history.append((next(iter(self.possible_words)), "GGGGG"))
                break

            assert len(self.possible_words) >= 1

        if len(self.possible_words) == 1:
            log(f"-> Answer found after {finished_rounds} rounds. The answer is {next(iter(self.possible_words))}")
        else:
            log(f"-> Answer not found after 6 rounds. The answer is {secret}")

        return finished_rounds

    def simulate(self, n=100, first_opener="TARES"):
        log("===== SIMULATION START =====")
        log("Press CTRL+C to terminate")
        try:
            self.first_opener = first_opener
            self.guess_histories = []
            self.time_taken = []
            self.games_played = 0
            for i in range(n):
                log(f"-> GAME {i}/{n}")
                timestamp = time.time_ns()

                self.reset()

                secret = random.choice(list(self.possible_words))
                guesses = self.play_one_game(secret)
                if guesses <= 6:
                    self.guess_histories.append(self.guess_history)
                    self.time_taken.append((time.time_ns() - timestamp) * 1e-9)
                self.games_played += 1
        except KeyboardInterrupt:
            pass  # intended way of terminating
        finally:  # potential race conditions on every variable but i dont care
            self.print_statistics()
            self.save_guess_histories()

if __name__ == "__main__":
    sim = WordleSimulator()
    sim.simulate(n=5, first_opener="TARES")
