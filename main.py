import json


with open("five_letter_words.json", "r") as f:
    five_letter_words = json.load(f)

black_chars = []
green_chars = [None]*5
yellow_chars = {}

for i in range(5):
    yellow_chars[i] = []

print("Note: Best openers are SALET, CRANE, etc")


def black_chars_check(chars: list, word: str):
    for char in chars:
        if char in word:
            return False
    return True


def yellow_chars_check(yellow_chars: dict, word: str):
    for pos in yellow_chars:
        if word[pos] in yellow_chars[pos]:
            return False
        for char in yellow_chars[pos]:
            if char not in word:
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


def sort_by_reference(reference_list: list, target_list: list):
    """
    Sorts target_list according to the order defined in reference_list.

    Parameters:
    - reference_list: List[str] — Defines the sorting order.
    - target_list: List[str] — Subset of strings to be ordered.

    Returns:
    - A new List[str] with elements of target_list sorted.

    Raises:
    - ValueError: if target_list has elements not present in reference_list.
    """
    target_list_copy = target_list.copy()

    # Build a position lookup for each element in reference_list
    position_map = {value: index for index, value in enumerate(reference_list)}

    # Check for unknown elements
    unknown_items = [item for item in target_list if item not in position_map]
    if unknown_items:
        # print(f"{unknown_items = }")
        for word in unknown_items:
            target_list_copy.remove(word)

    # Sort using the position in reference_list as the key
    return sorted(target_list_copy, key=lambda x: position_map[x]) + unknown_items


for i in range(6):
    word_input = input("The word: ")
    word_input = [i.lower() for i in word_input]

    green_chars_pos = input("Green characters positions [1-5] (eg. 135) (Press enter if nothing): ")
    green_chars_pos = [int(i)-1 for i in green_chars_pos]

    yellow_chars_pos = input("Yellow characters positions [1-5] (eg. 135) (Press enter if nothing): ")
    yellow_chars_pos = [int(i)-1 for i in yellow_chars_pos]

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
            to_remove_chars.append(word_input[pos])
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

    # print(five_letter_words)  # debug print

    with open("five_letter_words_order_by_freq.json", "r") as f:
        five_letter_words_order_by_freq = json.load(f)
        ordered_list = sort_by_reference(five_letter_words_order_by_freq, five_letter_words)

    print(f"Top {min(len(ordered_list), 20)} commonly used words that meet the criterias: \n{", ".join(ordered_list[:min(len(ordered_list), 20)])}")

    if len(five_letter_words) == 1:
        print(f"The word is: {five_letter_words[0]}")
        break
    elif len(five_letter_words) == 0:
        print("What on earth did you do?? Exiting!!")
        break
