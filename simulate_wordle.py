import random


def black_chars_check(chars: list, word: str):
    for char in chars:
        if char in word:
            return False
    return True


def yellow_chars_check(yellow_chars: dict, word: str):
    for pos in yellow_chars:
        if word[pos] in yellow_chars[pos]:
            return False
    return True


def green_chars_check(green_chars: list, word: str):
    for i in range(5):
        if not green_chars[i]:
            continue
        if green_chars[i] != word[i]:
            return False
    return True


def filter_words(black_chars, yellow_chars, green_chars, five_letter_words):
    possible_words = []
    for word in five_letter_words:
        if black_chars_check(black_chars, word) and yellow_chars_check(yellow_chars, word) and green_chars_check(green_chars, word):
            possible_words.append(word)
    
    return possible_words


black_chars = []
green_chars = [None]*5
yellow_chars = {}

for i in range(5):
    yellow_chars[i] = []


with open("five_letter_words.txt", "r") as f:
    persistent_five_letter_words = f.read().split("\n")


while 1:
    five_letter_words = persistent_five_letter_words.copy()
    answer = random.choice(five_letter_words)

    for _ in range(6):
        guessing_word = random.choice(five_letter_words)

        green_chars_pos = []
        yellow_chars_pos = []
        
        to_be_implicited_yellow_chars = []
        for i in range(5):
            if answer[i] == guessing_word[i]:
                green_chars_pos.append(i+1)
            elif guessing_word[i] in answer and guessing_word[i] not in to_be_implicited_yellow_chars:
                yellow_chars_pos.append(i+1)
                to_be_implicited_yellow_chars.append(guessing_word[i])

        green_chars_pos = "".join(green_chars_pos)
        yellow_chars_pos = "".join(yellow_chars_pos)

        to_remove_chars = []
        for pos in green_chars_pos:
            green_chars[pos] = word_input[pos]
            to_remove_chars.append(word_input[pos])
            for item in yellow_chars:
                if word_input[pos] in yellow_chars[item]:
                    yellow_chars[item].remove(word_input[pos])
        
        implicit_yellow_chars = []
        for pos in yellow_chars_pos:
            if word_input[pos] in green_chars:
                continue
            yellow_chars[pos] = list(set(yellow_chars[pos] + [word_input[pos]]))
            to_remove_chars.append(word_input[pos])
            implicit_yellow_chars.append(word_input[pos])
        
        for i in range(5):
            if word_input[i] in implicit_yellow_chars:
                yellow_chars[i] = list(set(yellow_chars[i] + [word_input[i]]))
            if green_chars[i]:
                yellow_chars[i] = []
        
        for char in to_remove_chars:
            word_input = [i for i in word_input if i != char]
        
        black_chars = list(set(black_chars + word_input))
        
        five_letter_words = filter_words(black_chars, yellow_chars, green_chars, five_letter_words)
    
    print(five_letter_words)
