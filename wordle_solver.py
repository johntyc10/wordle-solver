from base_wordle import BaseWordle, log

# tqdm fallback
try:
    from tqdm import tqdm
    print("Module tqdm is installed, loading bar will appear.")
except ImportError:
    print("Module tqdm is not detected, loading bar will be gone.")
    def tqdm(iterable, **kwargs):
        return iterable


class WordleSolver(BaseWordle):
    def __init__(self, use_tqdm = True):
        super().__init__(use_tqdm)

    def play(self, evaluate_entropy_in_first_round: bool = False):
        log("===== Wordle Solver (Entropy-based) =====")
        log(f"Recommended first guess: TARES, SALET, CRANE, etc")

        round_num = 1
        while len(self.possible_words) > 1 and round_num <= 6:
            log()
            log(f"--- Round {round_num} | {len(self.possible_words)} possible words ---")

            if round_num == 1 and not evaluate_entropy_in_first_round:
                best_guess = self.best_opener
                log("Recommended guess: TARES (entropy: 6.159)")
                log("2th guess: LARES (entropy: 6.115)")
                log("3th guess: RALES (entropy: 6.097)")
                log("4th guess: RATES (entropy: 6.084)")
                log("5th guess: RANES (entropy: 6.077)")
            else:
                log("Evaluating best guesses...")
                word_entropy = self.find_best_guesses()
                log("Done!")
                best_guess = word_entropy[0][0]
                log(f"Recommended guess: {best_guess} (entropy: {word_entropy[0][1]:.3f})")
                for i in range(1, min(5, len(word_entropy))):
                    word, entropy = word_entropy[i]
                    log(f"{i+1}th guess: {word} (entropy: {entropy:.3f})")

            if len(self.possible_words) <= 15:
                log("Remaining possibilities:", self.get_sorted_possible())

            log()

            # User input for guess
            while True:
                guess_input = input("What did you guess? (Enter = recommended): ").strip().upper()
                if not guess_input or self.is_in_word_list(guess_input):
                    guess = guess_input or best_guess
                    break
                log("Invalid input, please try again.")

            log(f"{guess} is chosen.")

            # User input for feedback
            while True:
                fb = input("Feedback (e.g. YGBBG, case insensitive): ").strip().upper()
                if len(fb) == 5 and self.is_valid_feedback(fb):
                    break
                log("Invalid input, please try again.")

            log(f"The feedback is {fb}.")

            self.update_possible_words(guess, fb)
            round_num += 1

        log()
        if len(self.possible_words) == 1:
            log(f"🎉 The answer is: {next(iter(self.possible_words))}")
        else:
            log("Remaining possibilities:", self.get_sorted_possible()[:30])


if __name__ == "__main__":
    solver = WordleSolver()
    solver.play()
