import nltk
import numpy as np
import pylab as pl
from collections import Counter
from nltk.corpus import brown

SCAN_WIDTH = 50

WIN_WIDTH = 1

NUM_BINS = 500


def make_word_list(filepath):  # turns txt file into all lower-case, all alphabetical characters, words split by ' '.

    txt_file = open(filepath, 'r')
    txt = txt_file.read()
    #txt = ' '.join(wordlst)

    txt_chars = []
    for c in txt:
        if c.isalpha():
            txt_chars.append(c.lower())
        else:
            txt_chars.append(' ')

    for i in range(len(txt_chars)-1):
        if txt_chars[i].isspace():
            if txt_chars[i+1].isspace():
                txt_chars[i] = ''

    new_txt = ''.join(txt_chars)

    word_list = new_txt.split(' ')

    return word_list


def get_norm_pair_corr(w_lst2, word2):

    instance_indexes = [q for q in range(len(w_lst2)) if w_lst2[q] == word2]
    complete_spacings = []

    for p in instance_indexes:
        if 99 < p < (len(w_lst2)- SCAN_WIDTH):
            for r in instance_indexes:
                if p != r:
                    if abs(p-r) <= SCAN_WIDTH:
                        complete_spacings.append(abs(p - r))

    return np.histogram(complete_spacings, bins=max(complete_spacings)-min(complete_spacings), density=True)


full_list = make_word_list('/Users/jmcrook/PycharmProjects/Word Spacings Project/KJB_clean.txt')

data = Counter(full_list)

X = []
for m in data.most_common(10):  # data.most_common(1) == ['word',count]

    word1 = m[0]

    pair_corr = get_norm_pair_corr(full_list, word1)

    mid = [0] * SCAN_WIDTH
    for i in range(len(pair_corr[1])-1):
        mid[int(pair_corr[1][i])] = pair_corr[0][i]
    mid[0] = word1

    X.append(mid)

    with open('pair_corr_data.csv', 'w') as d:
        d.write(''.join([(','.join([str(z) for z in M]) + '\n') for M in X]))

#y1 = [y for y in pair_corr[0]]
#x1 = [int(x) for x in pair_corr[1][:-1]]  # [WIN_SIZE:-(WIN_SIZE+1)]]

#print(x1)
#print(y1)
#print (y1_smooth)
#print(test_pair_corr)


#pl.plot(x1, y1)
#pl.show()

