import nltk
import numpy as np
import pylab as pl
from collections import Counter
from nltk.corpus import brown

SCAN_WIDTH = 25

WORD_NUM = 20


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
        if (SCAN_WIDTH-1) < p < (len(w_lst2)-SCAN_WIDTH):
            for r in instance_indexes:
                if p != r:
                    if abs(p-r) <= SCAN_WIDTH:
                        complete_spacings.append(abs(p - r))

    return np.histogram(complete_spacings, bins=max(complete_spacings)-min(complete_spacings), density=True)


full_list = norm_word_list(brown.words())

print "made the list"

data = Counter(full_list)

print "got data"

X = []
for m in data.most_common(50)[-20:]:  # data.most_common(1) == ['word',count]

    word1 = m[0]

    pair_corr = get_norm_pair_corr(full_list, word1)

    mid = [0] * SCAN_WIDTH
    for i in range(len(pair_corr[1])-1):
        mid[int(pair_corr[1][i])] = pair_corr[0][i]
    mid[0] = word1
    print word1
    X.append(mid)

ave_pair_corr = [0] * SCAN_WIDTH
ave_pair_corr[0] = 'ave'
for t in range(1, SCAN_WIDTH):
    for k in range(len(X)):
        ave_pair_corr[t] += X[k][t]
    ave_pair_corr[t] /= WORD_NUM
    print ave_pair_corr[t]

y1 = [y for y in ave_pair_corr[1:]]
x1 = [x for x in range(len(y1))]

#print(x1)
#print(y1)
#print (y1_smooth)
#print(test_pair_corr)


pl.plot(x1, y1)
pl.show()

