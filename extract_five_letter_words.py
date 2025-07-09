with open("words_alpha.txt", "r") as f:
    words = f.read().split("\n")

five_letter_words = []

for word in words:
    if len(word.strip()) == 5:
        five_letter_words.append(word.strip())

with open("five_letter_words.txt", "w") as f:
    f.write("\n".join(five_letter_words))
