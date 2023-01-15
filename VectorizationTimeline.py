import os
import sys
from progress.bar import IncrementalBar
import epitran
from epitran.backoff import Backoff
import time

# year_list = ["1720", "1730", "1740", "1750", "1760", "1770", "1780", "1830", "1840", "1850",
#              "1860", "1870", "1910", "1920", "1930", "1960", "1970", "1980", "2000", "2010", "2020"]
year_list = [ 
  "1700",
   "1710",
  "1720",
#  "1740", 
# "1750", "1760", "1770", "1780", "1830", 
"1840",
#  "1850",
             "1860", 
             "1870", 
            #  "1910", "1920", 
             "1930", 
            #  "1960", "1970", "1980",
            "1990",
             "2000", 
            # "2010", 
            #  "2020"
        ]

walk_dir = "Z:\\Projects\\IR\\Corpus\\English Novels\\"
#  = os.getcwd()
# for root, subdirs, files in os.walk(walk_dir):
#   for file in files:
#     if (file.split(".")[-1].lower() == 'txt'):
#       print(file)
global_token_list_link = "IPA03.csv"
global_set = set()


def add_to_dict(dic, elem):
    if elem in dic:
        dic[elem] += 1
    else:
        dic[elem] = 1
    return dic


for year in year_list:
    print("Working on " + year)

    to_unigram_link = "../Corpus/English Novels/"+year+"/unigram.csv"
    to_bigram_link = "../Corpus/English Novels/"+year+"/bigram.csv"
    to_trigram_link = "../Corpus/English Novels/"+year+"/trigram.csv"

    unigram = {}
    bigram = {}
    trigram = {}
    word_count = 0
    combined_tokenized_array = []
    print("Converting text to IPA")

    backoff = Backoff(['eng-Latn'])

    for root, subdirs, files in os.walk(walk_dir+year):
        for file in files:
            from_link = "../Corpus/English Novels/"+year+"/"+file
            to_link = "../Corpus/English Novels/"+year+"/"+"IPA_"+file+".txt"
            to_file = open(to_link, 'w', encoding="utf-8")
            from_file = open(from_link, 'r', encoding="utf-8")
            text = from_file.read()
            from_file.close()
            text1 = text.split(" ")
            bar = IncrementalBar('Countdown', max=len(text1))
            to_file_string = ""
            for word in text1:
                word = word.replace('"', '').replace("'", "").replace(
                    "(", "").replace(")", "").replace("[", "").replace("]", "").replace("`", "").replace(".", "")
                word = word.replace(";", "").replace(":", "").replace("!", "").replace(
                    ".", "").replace("“", "").replace("’", "").replace("”", "").replace("~", "")
                word = word.replace("-", "").replace("_",
                                                     "").replace(",", "").replace("?", "").replace("_", "").replace("-", "").replace("+", "").replace("=", "")
                for i in range(0, 10):
                    word = word.replace(str(i), '')
                new_word = ""
                for i in range(0, len(word)):
                    if ((ord(word[i]) < 97 or ord(word[i]) > 123) and (ord(word[i]) < 65 or ord(word[i]) >= 91)):
                        new_word += word[i]
                word = new_word
                if word == backoff.transliterate(word):
                    continue
                if (word != ""):
                    word_count += 1
                    tokenized_array = backoff.trans_list(word)
                    s = ''.join(tokenized_array)
                    combined_tokenized_array.extend(tokenized_array)
                    to_file_string += " " + s
                    # to_file.write(' ' + s)

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
                # print("Writing to file")
                to_file.write(to_file_string)
                to_file.close()
                # print("Writing to file finished")
    bar.finish()

    unigram_file = open(to_unigram_link, 'w', encoding="utf-8")
    for token in unigram:
        unigram_file.write(token+','+str(unigram[token])+'\n')
    unigram_file.close()

    bigram_file = open(to_bigram_link, 'w', encoding="utf-8")
    for token in bigram:
        bigram_file.write(token+','+str(bigram[token])+'\n')
    bigram_file.close()

    trigram_file = open(to_trigram_link, 'w', encoding="utf-8")
    for token in trigram:
        trigram_file.write(token+','+str(trigram[token])+'\n')
    trigram_file.close()

    no_of_phonemes = open(
        "../Output/English/" + year + "/no_phonemes.txt", 'w', encoding="utf-8")
    no_of_phonemes.write(str(len(unigram)))
    no_of_phonemes.close()

    word_counter = open(
        "../Output/English/" + year + "/word_count.txt", 'w', encoding="utf-8")
    word_counter.write(str(word_count))
    word_counter.close()


with open(global_token_list_link, 'w', encoding="utf-8") as global_token_list_file:
    global_token_list_file.write(str(global_set))
