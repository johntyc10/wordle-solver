#include <iostream>
#include <vector>
#include <array>
#include <fstream>
#include <cmath>
#include <algorithm>
#include <cassert>
using namespace std;

enum FeedbackColor {
    GREEN,
    YELLOW,
    BLACK
};

struct PatternCounts {
    vector<pair<int, int>> patternCounts;

    int patternDigest(array<FeedbackColor, 5>& feedback) {
        // assign a unique value for each feedback, like hash
        int digest = 0;
        for (int i = 0; i < 5; i++) {
            digest += feedback[i] * pow(10, i);
        }
        return digest;
    }

    void add(array<FeedbackColor, 5>& feedback) {
        int feedbackDigest = patternDigest(feedback);
        auto it = find(patternCounts.begin(), patternCounts.end(), feedbackDigest);

        if (it != patternCounts.end()){
            int index = distance(patternCounts.begin(), it);
            patternCounts[index].second++;
        } else
            patternCounts.push_back(make_pair(feedbackDigest, 1));
    }

    int getCountByIndex(int index) {
        return patternCounts[index].second;
    }

    int size() {
        return patternCounts.size();
    }
};

struct Top5BestGuesses {
    array<pair<string, double>, 5> topGuesses;
    int size = 0;

    void addIfTop5(pair<string, double> element) {
        if (size < 5) {
            topGuesses[size] = element;
            size++;
            return;
        }

        double entropy = element.second;

        for (int i = 0; i < size; i++) {
            if (entropy < topGuesses[i].second) {  // the lower the entropy, the better the guess
                insert(element, i);
                return;
            }
        }
    }

    void insert(pair<string, double> element, int index) {
        // insert element to index
        for (int i = size - 2; i >= index; i--) {
            topGuesses[i + 1] = topGuesses[i];
        }
        topGuesses[index] = element;
    }

    pair<string, double> get(int index) {
        // get element by index
        return topGuesses[index];
    }
};

class WordleSolver {
    vector<string> allWords;
    vector<string> possibleWords;

    public:
        vector<string> play() {
            cout << "===== Wordle Solver (C++ version) =====" << endl;
            cout << "Recommended first guess: TARES, SALET, CRANE, etc" << endl;
            cout << "Tip: TARES is the best first guess entropy-wise." << endl;

            int roundNum = 1;
            while (possibleWords.size() > 1 && roundNum <= 6) {
                cout << endl;
                cout << "--- Round " << roundNum << " | " << possibleWords.size() << " possible words ---" << endl;

                cout << "Evaluating best guesses..." << endl;
                Top5BestGuesses topGuesses = findBestGuesses();
                cout << "Done!" << endl;

                string topGuess = topGuesses.get(0).first;
                cout << "Top guess:\t" << topGuesses.get(0).first << " (entropy: " << topGuesses.get(0).second << ")" << endl;
                for (int i = 1; i < topGuesses.size; i++) {
                    string word = topGuesses.get(i).first;
                    double entropy = topGuesses.get(i).second;
                    cout << i + 1 << "th guess: " << word << " (entropy: " << entropy << ")" << endl;
                }

                cout << endl;

                // User input for guess
                string guessInput;
                while (1) {
                    cout << "What is your guess? (Enter = top): " << endl;
                    cin >> guessInput;
                    transform(guessInput.begin(), guessInput.end(), guessInput.begin(), ::toupper);
                    if (guessInput.empty() || isInWordList(guessInput)) {
                        break;
                    }
                    cout << "Invalid input, please try again.";
                }
                string guess;
                guess = (guessInput.empty()) ? topGuess : guessInput;

                cout << guess << " is chosen." << endl;

                // TODO: User input for feedback
            }
        }

        void debug() {
            cout << "WordleSolver.debug() called." << endl;
        }

    private:
        void loadWords() {
            ifstream answerListFile("./words/wordle-answers-alphabetical.txt");
            string word;
            while (getline(answerListFile, word)) {
                possibleWords.push_back(word);
            }
            cout << "Loaded " << possibleWords.size() << " words from answer list." << endl;

            ifstream wordListFile("./words/nyt-wordle-allowed-guesses-2026-03-06.txt");
            while (getline(wordListFile, word)) {
                allWords.push_back(word);
            }
            cout << "Loaded " << allWords.size() << " words from word list." << endl;
        }

        array<FeedbackColor, 5> getFeedback(string guess, string secret) {
            // return the official nyt wordle feedback of guess if secret were the secret word.
            array<FeedbackColor, 5> result;
            result.fill(BLACK);

            array<int, 26> secretCount{};  // keeps track of which letters should be assigned yellow for secretCount[letter] times
            for (int i = 0; i < 5; i++) {
                if (guess[i] == secret[i])
                    result[i] = GREEN;
                else
                    secretCount[secret[i] - 'A'] += 1;
            }

            for (int i = 0; i < 5; i++) {
                if (result[i] == BLACK) {
                    char letter = guess[i];
                    if (secretCount[letter - 'A'] > 0) {
                        result[i] = YELLOW;
                        secretCount[letter - 'A']--;
                    }
                }
            }

            return result;
        }

        void updatePossibleWords(string guess, array<FeedbackColor, 5> feedback) {
            int i = 0;
            while (i < possibleWords.size()) {
                if (getFeedback(guess, possibleWords[i]) != feedback) {
                    possibleWords.erase(possibleWords.begin() + i);
                    continue;  // not incrementing i
                }
                i++;
            }
        }

        double computeEntropy(string guess) {
            // shannon entropy for a guess.
            assert(!possibleWords.empty());

            PatternCounts patternCounts;
            for (auto secret : possibleWords) {
                array<FeedbackColor, 5> fb = getFeedback(guess, secret);
                patternCounts.add(fb);
            }

            int total = patternCounts.size();
            double entropy = 0.0;
            for (int i = 0; i < total; i++) {
                int count = patternCounts.getCountByIndex(i);
                double p = count / (double) total;
                entropy -= p * log2(p);
            }

            return entropy;
        }

        Top5BestGuesses findBestGuesses() {
            assert(!possibleWords.empty());

            Top5BestGuesses topGuesses;
            for (string candidate : allWords) {
                double entropy = computeEntropy(candidate);
                topGuesses.addIfTop5(make_pair(candidate, entropy));
            }

            return topGuesses;
        }

        bool isInWordList(string word) {
            auto it = find(allWords.begin(), allWords.end(), word);
            return it == allWords.end();
        }
};


int main() {
    WordleSolver solver;
    solver.debug();
}
