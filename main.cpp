#include <iostream>
#include <vector>
#include <array>
#include <fstream>
#include <cmath>
#include <algorithm>
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

class WordleSolver {
    vector<string> answerList;
    vector<string> wordList;

    public:
        vector<string> play();

        void debug() {
            cout << "WordleSolver.debug() called." << endl;
        }

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

        void updateWordList(string guess, array<FeedbackColor, 5> feedback) {
            int i = 0;
            while (i < wordList.size()) {
                if (getFeedback(guess, wordList[i]) != feedback) {
                    wordList.erase(wordList.begin() + i);
                    continue;  // not incrementing i
                }
                i++;
            }
        }

        double computeEntropy(string guess) {
            // shannon entropy for a guess.
            if (wordList.empty())
                return 0.0;

            PatternCounts patternCounts;
            for (auto secret : wordList) {
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
};


int main() {
    WordleSolver solver;
    solver.debug();
}
