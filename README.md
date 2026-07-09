# The Wordle Solver

A wordle solver that uses information theory approach to effectively solve the game of wordle.

The word list is pulled directly from the nytimes wordle source code, see https://www.nytimes.com/games-assets/v2/62.dd5228399a9dc7141388.js. Please do not hesitate to inform me if there is a more accurate word list(s).

## The Algorithm

In each round of the game:
1. Prompts the user which word they guesses
2. Gets the feedback of the word (eg. YGBBG)
3. Evaluate the list of remaining possible words
4. Select a word (from all words) that maximizes the entropy for the remaining possible words (ie. select a word that on average eliminates the most remaining words)
    - Entropy formula: $$H = -\sum_{i} p_i \times log_2(p_i)$$
5. Repeat until only one possible word is left or the game is over

## Performance

This solver yields 100% success rate with ~650 trials of games.

For simulating 10000 games, here is the statistics report:

```
===== STATISTICS REPORT =====
First opener used: TARES (Max entropy)
Guesses taken distribution:
1: 19
2: 1110
3: 5279
4: 3124
5: 434
6: 33
Average guesses taken: 3.294
Average time taken per game: 5.211s
Average time taken per round: 1.582s
Success rate: 99.990% (9999/10000)
```

The word that the solver failed to solve is ZILLS.

## How to use

1. Clone the repository:
```bash
git clone https://github.com/johntyc10/wordle-solver.git && cd wordle-solver
```

2. Install tqdm module
```bash
pip install tqdm  # or any other methods of your liking
```

3. Run wordle_solver.py
```bash
python wordle_solver.py
```
