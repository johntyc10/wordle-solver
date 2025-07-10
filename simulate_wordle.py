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


def average(list_of_num: list):
    if len(list_of_num) == 0:
        return 0
    return sum(list_of_num) / len(list_of_num)


with open("five_letter_words.txt", "r") as f:
    persistent_five_letter_words = f.read().split("\n")


success_round_count = 0
possibilities_left = []


round_count = 1

while 1:
    black_chars = []
    green_chars = [None]*5
    yellow_chars = {}

    for i in range(5):
        yellow_chars[i] = []

    five_letter_words = persistent_five_letter_words.copy()
    answer = random.choice(five_letter_words)
    sequence_of_guessing_words = []

    for att in range(6):
        guessing_word = random.choice(five_letter_words) if att != 0 else "salet"
        sequence_of_guessing_words.append(guessing_word)

        green_chars_pos = []
        yellow_chars_pos = []
        
        to_be_implicited_yellow_chars = []
        for i in range(5):
            if answer[i] == guessing_word[i]:
                green_chars_pos.append(i)
            elif guessing_word[i] in answer and guessing_word[i] not in to_be_implicited_yellow_chars:
                yellow_chars_pos.append(i)
                to_be_implicited_yellow_chars.append(guessing_word[i])

        # green_chars_pos = "".join([str(i) for i in green_chars_pos])
        # yellow_chars_pos = "".join(str(i) for i in yellow_chars_pos)

        word_input = [i.lower() for i in guessing_word]

        # print(word_input)
        # print(answer)

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

        # print(black_chars)
        # print(yellow_chars)
        # print(green_chars)
        # print(five_letter_words)
        
        five_letter_words = filter_words(black_chars, yellow_chars, green_chars, five_letter_words)
        if len(five_letter_words) == 1:
            break
    
        # print(five_letter_words)
    
    if round_count % 100 == 0:
        if len(five_letter_words) <= 5:
            print(f"Round {round_count} used {len(sequence_of_guessing_words)} attempts to guess the word \"{answer}\".")
            success_round_count += 1
        else:
            print(f"Round {round_count} used all 6 attempts but did not guess the word \"{answer}\". There are {len(five_letter_words)} possibilities left.")
            possibilities_left.append(len(five_letter_words))

        print(f"Sequence of guessing words: {', '.join(sequence_of_guessing_words)}")
        print(f"Success rate: {round(success_round_count / round_count * 100, 2)}%")
        print(f"Average possibilities left: {round(average(possibilities_left), 2)}")

    round_count += 1
