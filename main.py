with open("five_letter_words.txt", "r") as f:
    five_letter_words = f.read().split("\n")

not_contain_chars = []
contain_chars = [None]*5


def contains(chars: list, word: str):
    for char in chars:
        if char in word:
            return True
    return False


def compare_word(contain_chars: list, word: str):
    for i in range(5):
        if not contain_chars[i]:
            continue
        if contain_chars[i] != word[i]:
            return False
    return True


def filter_words(not_contain_chars, contain_chars, five_letter_words):
    return_value = []
    for word in five_letter_words:
        print(word, contains(not_contain_chars, word), compare_word(contain_chars, word))
        if not contains(not_contain_chars, word) and compare_word(contain_chars, word):
            return_value.append(word)
    
    return return_value


while 1:
    not_contain_char_input = input("Not contain chars (a,b,c) >> ")
    not_contain_char_input = not_contain_char_input.replace(" ", "")
    not_contain_chars = list(set(not_contain_char_input.split(",") + not_contain_chars))

    contain_char_input = input("Contain chars (a1,b2,c3) >> ")
    contain_char_input = contain_char_input.replace(" ", "")
    contain_char_input = contain_char_input.split(",")
    for thing in contain_char_input:
        if thing:
            contain_chars[int(thing[1])-1] = thing[0]
    
    print(not_contain_chars)
    print(contain_chars)
    
    five_letter_words = filter_words(not_contain_chars, contain_chars, five_letter_words)

    print(five_letter_words)
    