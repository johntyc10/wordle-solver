# The Wordle Solver

This solves wordle using information theory approach, namely maximizing entropy for the guess each round.

The word list is pulled directly from the nytimes wordle source code, see https://www.nytimes.com/games-assets/v2/62.dd5228399a9dc7141388.js. Please inform me if there is a more updated word list.

This solver yields 100% success rate with ~650 trials of games.

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
