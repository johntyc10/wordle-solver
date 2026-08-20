#include <iostream>
#include <vector>
#include <array>
#include <fstream>
#include <cmath>
#include <algorithm>
#include <cassert>
#include <unordered_map>
using namespace std;

enum FeedbackColor {
    GREEN,
    YELLOW,
    BLACK
};

enum Difficulty {
    EASY,
    HARD
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
            if (entropy > topGuesses[i].second) {
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
    Difficulty difficulty;
    array<string, 2> difficultyString;

    public:
        void play() {
            init();
            cout << endl;

            cout << "===== Wordle Solver (C++ version) =====" << endl;
            cout << "Recommended first guess: TARES, SALET, CRANE, etc" << endl;
            cout << "Tip: TARES is the best first guess entropy-wise." << endl;

            while (1) {
                string _ans;
                cout << "Play in hard mode? [y/N]: ";
                getline(cin, _ans);
                if (_ans == "Y" || _ans == "y") {
                    difficulty = HARD;
                    break;
                }
                else if (_ans.empty() || _ans == "N" || _ans == "n") {
                    difficulty = EASY;
                    break;
                }
                else {
                    cout << "Invalid input, please input either \"y\" or \"n\"." << endl;
                }
            }

            cout << endl;
            cout << "Playing wordle in " << difficultyString[difficulty] << " mode." << endl;

            int roundNum = 1;
            while (possibleWords.size() > 1 && roundNum <= 6) {
                cout << endl;
                cout << "--- Round " << roundNum << " | " << possibleWords.size() << " possible words (" << difficultyString[difficulty] << " mode) ---" << endl;

                string topGuess;
                if (roundNum == 1) {
                    topGuess = "TARSE";
                    cout << "Top guess: TARSE (entropy: 5.94673)" << endl;
                    cout << "2th guess: TIARE (entropy: 5.9312)" << endl;
                    cout << "3th guess: SOARE (entropy: 5.88596)" << endl;
                    cout << "4th guess: ROATE (entropy: 5.88278)" << endl;
                    cout << "5th guess: RAISE (entropy: 5.87791)" << endl;
                } else {
                    cout << "Evaluating best guesses..." << endl;
                    Top5BestGuesses topGuesses = findBestGuesses(difficulty);
                    cout << "Done!" << endl;

                    topGuess = topGuesses.get(0).first;
                    cout << "Top guess: " << topGuesses.get(0).first << " (entropy: " << topGuesses.get(0).second << ")" << endl;
                    for (int i = 1; i < topGuesses.size; i++) {
                        string word = topGuesses.get(i).first;
                        double entropy = topGuesses.get(i).second;
                        cout << i + 1 << "th guess: " << word << " (entropy: " << entropy << ")" << endl;
                    }
                }
                cout << endl;


                // User input for guess
                string guessInput;
                while (1) {
                    cout << "What is your guess? (Enter = top): ";
                    getline(cin, guessInput);
                    transform(guessInput.begin(), guessInput.end(), guessInput.begin(), ::toupper);
                    if (guessInput.empty() || isInWordList(guessInput)) {
                        break;
                    }
                    cout << "Invalid input, please try again." << endl;
                }
                string guess;
                guess = (guessInput.empty()) ? topGuess : guessInput;

                cout << guess << " is chosen." << endl;

                // User input for feedback
                string fbInput;
                while (1) {
                    cout << "Feedback (e.g. YGBBG, case insensitive): ";
                    getline(cin, fbInput);
                    transform(fbInput.begin(), fbInput.end(), fbInput.begin(), ::toupper);
                    if (isValidFeedback(fbInput)) {
                        break;
                    }
                    cout << "Invalid input, please try again." << endl;
                }

                if (fbInput == "GGGGG") {
                    cout << "GGs! Nice work!" << endl;
                } else {
                    cout << "Your feedback input is " << fbInput << endl;
                }

                array<FeedbackColor, 5> fb;
                for (int i = 0; i < 5; i++) {
                    if (fbInput[i] == 'G')
                        fb[i] = GREEN;
                    else if (fbInput[i] == 'Y')
                        fb[i] = YELLOW;
                    else if (fbInput[i] == 'B')
                        fb[i] = BLACK;
                    else {
                        cerr << "Invalid feedback" << endl;
                        exit(1);
                    }
                }

                updatePossibleWords(guess, fb);
                roundNum += 1;
            }

            cout << endl;
            if (possibleWords.size() == 1) {
                cout << "The answer is: " << possibleWords[0] << endl;
            } else {
                cout << "No possible words are left. Check your input and try again." << endl;
            }
        }

        void debug() {
            cout << "WordleSolver.debug() called." << endl;
            cout << isValidFeedback("BBBBB") << endl;
            cout << isValidFeedback("BBGGB") << endl;
            cout << isValidFeedback("HHHHH") << endl;
        }

    private:
        void init() {
            loadWords();
            difficultyString[EASY] = "EASY";
            difficultyString[HARD] = "HARD";
        }

        void loadWords() {
            ifstream answerListFile("./words/wordle-answers-alphabetical.txt");
            string word;
            while (getline(answerListFile, word)) {
                transform(word.begin(), word.end(), word.begin(), ::toupper);
                possibleWords.push_back(word);
            }
            cout << "Loaded " << possibleWords.size() << " words from answer list." << endl;

            ifstream wordListFile("./words/nyt-wordle-allowed-guesses-2026-03-06.txt");
            while (getline(wordListFile, word)) {
                transform(word.begin(), word.end(), word.begin(), ::toupper);
                allWords.push_back(word);
            }
            cout << "Loaded " << allWords.size() << " words from word list." << endl;
        }

        array<FeedbackColor, 5> getFeedback(string guess, string secret) {
            // return the official nyt wordle feedback of guess if secret were the secret word.
            array<FeedbackColor, 5> result;
            result.fill(BLACK);

            array<int, 26> secretCount;  // keeps track of which letters should be assigned yellow for secretCount[letter] times
            secretCount.fill(0);
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

            unordered_map<int, int> feedbackCounts;
            for (auto secret : possibleWords) {
                array<FeedbackColor, 5> fb = getFeedback(guess, secret);
                int fbDigest = feedbackDigest(fb);
                if (feedbackCounts.contains(fbDigest)) {
                    feedbackCounts[fbDigest]++;
                } else {
                    feedbackCounts[fbDigest] = 1;
                }
            }

            double total = (double) possibleWords.size();
            double entropy = 0.0;
            for (const auto& [fb, count] : feedbackCounts) {
                double p = count / total;
                entropy -= p * log2(p);
            }

            return entropy;
        }

        int feedbackDigest(array<FeedbackColor, 5> feedback) {
            int digest = 0;
            for (int i = 0; i < feedback.size(); i++) {
                digest += feedback[i] * (int) pow(10, i);
            }
            return digest;
        }

        Top5BestGuesses findBestGuesses(Difficulty difficulty) {
            assert(!possibleWords.empty());
            assert(!allWords.empty());

            vector<string> candidateWords = (difficulty == EASY) ? allWords : possibleWords;

            int progress = 0;
            Top5BestGuesses topGuesses;
            for (string candidate : candidateWords) {
                double entropy = computeEntropy(candidate);
                topGuesses.addIfTop5(make_pair(candidate, entropy));
                progress++;
                if (progress % 1000 == 1 || progress == candidateWords.size()) {
                    cout << "\33[2K\r";  // clear current line
                    cout << "Progress: " << progress << "/" << candidateWords.size() << " (" << progress / (double) candidateWords.size() * 100 << "%)";
                    cout.flush();
                }
            }
            cout << endl;

            return topGuesses;
        }

        bool isInWordList(string word) {
            auto it = find(allWords.begin(), allWords.end(), word);
            return it != allWords.end();
        }

        bool isValidFeedback(string feedback) {
            if (feedback.size() != 5) {
                return false;
            }

            for (char letter : feedback) {
                if (
                    letter != 'G' &&
                    letter != 'Y' &&
                    letter != 'B'
                ) {
                    return false;
                }
            }

            return true;
        }
};


int main() {
    WordleSolver solver;
    solver.play();
}
