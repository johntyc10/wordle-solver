# The Wordle Solver

A wordle solver that uses information theory approach to effectively solve the game of wordle.

The wordle answers and allowed guesses are from https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b and https://gist.github.com/cfreshman/8b92bc418b43096094cf5d1b0eea8f84 respectively.

Please do not hesitate to inform me if there are more accurate word lists.

## The Algorithm

In each round of the game:
1. Prompts the user which word they guesses
2. Gets the feedback of the word (eg. YGBBG)
3. Evaluate the list of remaining possible words
4. Select a word (from all words) that maximizes the entropy for the remaining possible words (ie. select a word that on average eliminates the most remaining words)
    - Entropy formula: $$H = -\sum_{i} p_i \times log_2(p_i)$$
5. Repeat until only one possible word is left or the game is over

## Performance

This solver yields 100% success rate for all 2315 words.

Here is the complete statistics report:
```
===== STATISTICS REPORT =====
First opener used: TARES
Guesses taken distribution:
1: 0
2: 26
3: 874
4: 1309
5: 102
6: 4
Average guesses taken: 3.647516198704104
Average time taken per game: 1.917801373360224s
Average time taken per round: 0.5257828255955611s
Success rate: 100.0% (2315/2315)
```

## How to use

1. Clone the repository:
```bash
git clone https://github.com/johntyc10/wordle-solver.git && cd wordle-solver
```

2. (Optional) Install tqdm module
```bash
pip install tqdm  # or any other methods of your liking
```

3. Run wordle_solver.py
```bash
python wordle_solver.py
```

## Contribute
Please do not hesitate to open an issue or a PR request!
