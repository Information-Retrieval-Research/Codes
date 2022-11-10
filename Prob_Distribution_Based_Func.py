import pandas as pd
import numpy as np
import math
# 1 - KL Divergence Function
'''
x=len(unigram_list) #or x=len(phonemes_list)
for i in range(x-1):
    for j in range(i+1,x):
        dict1 = lang_list[i]
kl_divergence(dict1, dict2)
'''


def kl(dict1, dict2):
    '''
    This function needs two hashmap which have to be converted to their probabilities.
    '''
    list1 = []
    list2 = []
    for i in dict1.keys():
        list1.append(dict1[i])
        list2.append(dict2[i])

    return sum(list1[i]*np.log(list1[i]/list2[i]) for i in range(len(list1)) if list1[i] > 0 and list2[i] > 0)

# 2 - L1 Normalization


def l1(dict1, dict2):
    list1 = []
    list2 = []
    for i in dict1.keys():
        list1.append(dict1[i])
        list2.append(dict2[i])
    p1 = np.array(list1)
    p2 = np.array(list2)

    point1 = np.array(p1)
    point2 = np.array(p2)
    difference = point1 - point2
    l1norm = np.linalg.norm(difference, ord=1)
    return l1norm

# 3 - L2 Normalization


def l2(dict1, dict2):
    list1 = []
    list2 = []

    for i in dict1.keys():
        list1.append(dict1[i])
        list2.append(dict2[i])

    p1 = np.array(list1)
    p2 = np.array(list2)

    point1 = np.array(p1)
    point2 = np.array(p2)
    difference = point1 - point2
    l2norm = np.linalg.norm(difference, ord=2)
    return l2norm

# 4 Rao Divergence


def alpha(list1, list2):
    return sum(math.sqrt(list1[i]*list2[i]) for i in range(len(list1)) if list1[i] > 0 and list2[i] > 0)


def beta(list1, list2):
    return sum(math.sqrt(list1[i]*list2[i]) * math.log2(list1[i]/list2[i]) for i in range(len(list1)) if list1[i] > 0 and list2[i] > 0)


def gamma(list1, list2):
    return sum(math.sqrt(list1[i]*list2[i]) * (math.log2(list1[i]/list2[i]))**2 for i in range(len(list1)) if list1[i] > 0 and list2[i] > 0)

# define distributions


def rao(dict1, dict2):
    list1 = []
    list2 = []

    for i in dict1.keys():
        list1.append(dict1[i])
        list2.append(dict2[i])
    # calculate (list1 || list2)

    a = alpha(list1, list2)
    b = beta(list1, list2)
    c = gamma(list1, list2)
    D = math.sqrt((a*c-b**2)/a**2)

    return D


def dot_product(dict1, dict2):
    dot_prod = 0
    root1 = 0
    root2 = 0
    for i in dict1.keys():
        dot_prod += dict1[i]*dict2[i]
        root1 += dict1[i]**2
        root2 += dict2[i]**2
    
    root1 = math.sqrt(root1)
    root2 = math.sqrt(root2)
    return dot_prod/(root1*root2)


def normalise(dictionary):
    total_freq = 0
    for ipa in dictionary.keys():
        total_freq += int(dictionary[ipa])
    for ipa in dictionary.keys():
        dictionary[ipa] = int(dictionary[ipa])/total_freq
    return dictionary


def equalise(dict1, dict2):
    ipa_list = set()
    for i in dict1.keys():
        ipa_list.add(i)
    for i in dict2.keys():
        ipa_list.add(i)

    for ipa in ipa_list:
        if (ipa not in dict1):
            dict1[ipa] = 0
        if (ipa not in dict2):
            dict2[ipa] = 0
    return (dict1, dict2)


language_dict = {
    "Bengali": ["ben-Beng", "ben-Beng-red"],
    "Hindi": ["hin-Deva"],
    "Malayalam": ["mal-Mlym"],
    "Marathi": ["mar-Deva"],
    "Oriya": ["ori-Orya"],
    "Punjabi": ["pan-Guru"],
    "Tamil": ["tam-Taml", "tam-Taml-red"],
    "Telugu": ["tel-Telu"],
    "Urdu": ["urd-Arab"]
}

language_list = []
for lang in language_dict.keys():
    language_list.append(lang)

gram_list = ["unigram", "bigram", "trigram"]

normalised_dict = {}

for gram in gram_list:
    print("Working with "+gram+"....")
    for i in range(0, len(language_list)):
        print("Working with "+language_list[i]+"....")
        f1 = open("../Output/Languages/" +
                  language_list[i]+"/"+gram+"02.csv", "r", encoding="utf-8")
        text1 = f1.readlines()
        dict1 = {}
        for lines in text1:
            if (lines != ""):
                try:
                    dict1[lines.split(",")[0]] = lines.split(",")[1]
                except:
                    pass
        f1.close()
        dict1 = normalise(dict1)
        normalised_dict[language_list[i]+"_"+gram] = dict1
    print(gram + " normalised")

to_csv = {"gram": [], "language1": [], "language2": [],
          "l1": [], "l2": [],  "kl": [], "rao": [], "dot_product": []}
# to_csv = {"language1": [], "language2": [], "l1": [], "l2": [], "rao": [], "kl": []}


for gram in gram_list:
    for i in range(0, len(language_list)):
        dict1 = normalised_dict[language_list[i]+"_"+gram]

        for j in range(i, len(language_list)):
            dict2 = normalised_dict[language_list[j]+"_"+gram]
            dict1, dict2 = equalise(dict1, dict2)
            print("Working with " + gram + " of " +
                  language_list[i]+" and "+language_list[j]+"....")
            # open("../Output/Languages/")
            to_csv["gram"].append(gram)
            to_csv["language1"].append(language_list[i])
            to_csv["language2"].append(language_list[j])
            to_csv["l1"].append(l1(dict1, dict2))
            to_csv["l2"].append(l2(dict1, dict2))
            to_csv["rao"].append(rao(dict1, dict2))
            to_csv["kl"].append(kl(dict1, dict2))
            to_csv["dot_product"].append(dot_product(dict1, dict2))

to_csv_dataframe = pd.DataFrame.from_dict(to_csv)
print(to_csv_dataframe)
to_csv_dataframe.to_csv('prob_distribution_summary02.csv')
