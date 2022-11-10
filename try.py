word = "नमस्तेhey"
new_word = ""
for i in range(0, len(word)):
    if ((ord(word[i]) < 97 or ord(word[i]) > 123) and (ord(word[i]) < 65 or ord(word[i]) >= 91)):
        new_word += word[i]

print(new_word)
