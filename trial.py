import time
from progress.bar import IncrementalBar
import epitran
from epitran.backoff import Backoff

language_list = {"Amharic" :["amh-Ethi","amh-Ethi-pp","amh-Ethi-red"]}


def word_to_token(word, lang_list):
    backoff = Backoff(lang_list)

    return backoff.trans_list(word)


def add_to_dict(dic, elem):
    if elem in dic:
        dic[elem] += 1
    else:
        dic[elem] = 1
    return dic

global_token_list_link = "IPA.txt"
global_set = set()
with open(global_token_list_link, 'r' ,encoding = "utf-8") as global_token_list_file:
  init_global_string = global_token_list_file.read()
  # global_token_list_file.truncate(0)
  global_list = init_global_string.split(",")
  for i in global_list:
    global_set.add(i)


for language in language_list:
    print(f"Working on {language}...")
    from_link = f"../Corpus/Languages/{language}/{language}.txt"
    to_link = f"../Corpus/Languages/{language}/IPA.txt"

    to_unigram_link = f"../Output/Languages/{language}/unigram.csv"
    to_bigram_link = f"../Output/Languages/{language}/bigram.csv"
    to_trigram_link = f"../Output/Languages/{language}/trigram.csv"

    from_file = open(from_link, 'r', encoding="utf-8")
    to_file = open(to_link, 'a', encoding="utf-8")
    text = from_file.read()

    unigram = {}
    bigram = {}
    trigram = {}
    word_count = 0
    combined_tokenized_array = []
    print("Converting text to IPA...")
    text1 = text.split(" ")
    bar = IncrementalBar('Countdown', max = len(text1))

    for word in text1:
        word_count += 1
        tokenized_array = word_to_token(word, language_list[language])
        s = ''.join(tokenized_array)
        combined_tokenized_array.extend(tokenized_array)
        to_file.write(' ' + s)

        # TO Write to the global list of unique token
        for token in tokenized_array:
            global_set.add(token)

        # Create Unigram
        for token in tokenized_array:
            unigram = add_to_dict(unigram, token)

        # Create Bigram
        for i in range(len(tokenized_array)):
            if i >= 1:
                token = tokenized_array[i-1] + tokenized_array[i]
                bigram = add_to_dict(bigram, token)

        # Create trigram
        for i in range(len(tokenized_array)):
            if i >= 2:
                token = tokenized_array[i-2] + \
                    tokenized_array[i-1] + tokenized_array[i]
                trigram = add_to_dict(trigram, token)
        bar.next()
    bar.finish()
    unigram_file = open(to_unigram_link, 'w', encoding="utf-8")
    for token in unigram:
        unigram_file.write(token+','+unigram[token]+'\n')

    bigram_file = open(to_bigram_link, 'w', encoding="utf-8")
    for token in bigram:
        bigram_file.write(token+','+unigram[token]+'\n')

    trigram_file = open(to_trigram_link, 'w', encoding="utf-8")
    for token in trigram:
        trigram_file.write(token+','+unigram[token]+'\n')

    no_of_phonemes = open(
        f"../Output/Languages/{language}/no_phonemes.txt", 'w', encoding="utf-8")
    no_of_phonemes.write(str(len(unigram)))

    word_counter = open(
        f"../Output/Languages/{language}/word_count.txt", 'w', encoding="utf-8")
    word_counter.write(str(word_count))
    
