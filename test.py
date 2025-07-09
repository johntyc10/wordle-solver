def compare_word(contain_chars: list, word: str):
    for i in range(5):
        if not contain_chars[i]:
            continue
        if contain_chars[i] != word[i]:
            return False
    return True


lst = [None]*5
lst[1] = "i"
lst[3] = "g"
print(compare_word(lst, "niaaa"))