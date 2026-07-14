from typing import List, Dict, Tuple, Set, Iterable
import random
import time
import copy
from wordle_solver import BaseWordle, log
from datetime import datetime, timedelta
from pathlib import Path
import json

def avg(x: Iterable):
    if len(x) == 0:
        return 0
    return sum(x) / len(x)

class WordleSolverBenchmark(BaseWordle):
    def __init__(self, use_tqdm = False):
        super().__init__(use_tqdm)

        self.all_words_persistence: List[str] = self._load_words(self.all_words_path)
        self.possible_words_persistence: Set[str] = set(self._load_words(self.possible_words_path))
        self.possible_words_list = self._load_words(self.possible_words_path)

    def reset(self):
        self.all_words = copy.deepcopy(self.all_words_persistence)
        self.possible_words = copy.deepcopy(self.possible_words_persistence)
        self.guess_history: List[Tuple[str, str]] = []

    def save_statistics(self):
        filename = f"benchmark_guess_histories.json"
        dir = Path(f"./output/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}")
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

        log(f"Average guesses taken: {avg(guesses_taken)}")
        log(f"Average time taken per game: {avg(self.time_taken)}s")
        log(f"Average time taken per round: {sum(self.time_taken) / sum(guesses_taken)}s")
        log(f"Success rate: {len(guesses_taken) / self.games_played * 100}% ({len(guesses_taken)}/{self.games_played})")  # couldnt care less about ZeroDivisionError here

        log()
        log(f"Start time: {datetime.fromtimestamp(self.start_time).strftime("%Y/%m/%d, %H:%M:%S")}")
        log(f"End time: {datetime.now().strftime("%Y/%m/%d, %H:%M:%S")}")
        log(f"Time taken: {timedelta(seconds=time.time() - self.start_time)}")


    def play_one_game(self, secret: str) -> bool:
        """
        Simulates playing one game of wordle using optimal approach.
        secret: wordle answer
        Returns True if the solver successfully solved the wordle, returns False otherwise.
        """
        success = False
        for round_num in range(1, 7):
            log(f"  => Playing round {round_num} ({len(self.possible_words)} words left)")

            if round_num == 1:
                best_guess = self.first_opener
            else:
                word_entropy = self.find_best_guesses()
                best_guess = word_entropy[0][0]

            # Simulate user input
            guess = best_guess

            fb = self.get_feedback(guess, secret)

            self.update_possible_words(guess, fb)
            assert len(self.possible_words) >= 1

            if len(self.possible_words) == 1:
                # play one more round of correct answer as guess
                if round_num <= 5:
                    self.guess_history.append((next(iter(self.possible_words)), "GGGGG", 1))
                    success = True
                break

        if success:
            log(f"-> Answer found after {len(self.guess_history)} rounds. The secret is {next(iter(self.possible_words))}")
        else:
            log(f"-> Answer not found after 6 rounds.")

        return success

    def run(self, first_opener="TARES"):
        log("===== BENCHMARK START =====")
        log("Press CTRL+C to terminate")
        try:
            self.start_time = time.time()

            self.first_opener = first_opener
            self.guess_histories = []
            self.time_taken = []
            self.games_played = 0

            n = len(self.possible_words_list)
            for i in range(n):
                self.reset()

                secret = self.possible_words_list[i]
                log(f"-> GAME {i}/{n} (secret: {secret})")

                timestamp = time.time()
                success = self.play_one_game(secret)
                if success:
                    self.guess_histories.append(self.guess_history)
                    self.time_taken.append(time.time() - timestamp)
                self.games_played += 1
        except KeyboardInterrupt:
            pass  # intended way of terminating
        finally:  # potential race conditions on every variable but i dont care
            self.print_statistics()
            self.save_statistics()

if __name__ == "__main__":
    benchmark = WordleSolverBenchmark()
    benchmark.run(first_opener="TARES")  # TODO: accept arguments in command line
