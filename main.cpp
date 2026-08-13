#include <iostream>
#include <vector>
#include <array>
#include <fstream>
using namespace std;

enum FeedbackColor {
    GREEN,
    YELLOW,
    BLACK
};

class WordleSolver {
    vector<string> answerList;
    vector<string> wordList;

    public:
        vector<string> play();

        void debug();

    private:
        void loadWords() {
            ifstream answerListFile("./words/wordle-answers-alphabetical.txt");
            string word;
            while (getline(answerListFile, word)) {
                answerList.push_back(word);
            }
            cout << "Loaded " << answerList.size() << " words from answer list." << endl;

            ifstream wordListFile("./words/nyt-wordle-allowed-guesses-2026-03-06.txt");
            while (getline(wordListFile, word)) {
                wordList.push_back(word);
            }
            cout << "Loaded " << wordList.size() << " words from word list." << endl;
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
};


int main() {
    WordleSolver solver;
    solver.debug();
}
