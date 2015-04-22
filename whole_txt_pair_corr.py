import nltk
import numpy as np
import pylab as pl
from nltk.corpus import brown, stopwords


SCAN_WIDTH = 20

conj = ['and', 'or', 'but', 'for', 'nor', 'yet', 'so']


def make_word_list(filepath):  # normalizes a txt

    txt_file = open(filepath, 'r')
    txt = txt_file.read()
    #txt = ' '.join(wordlst)  # if input is a list

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


def get_pair_corr_fast(w_lst3):

    pair_corr_spacings = []

    length = len(w_lst3)

    for w in range(SCAN_WIDTH, len(w_lst3)-SCAN_WIDTH):
        print float(w)/length
        for p in range(w-SCAN_WIDTH, w + SCAN_WIDTH + 1):
            if w != p:
                if w_lst3[w] == w_lst3[p]:
                    pair_corr_spacings.append(abs(w-p))

    return np.histogram(pair_corr_spacings, bins=range(SCAN_WIDTH+2), density=True)  # the +2 is because the we're
                                                                                     # defining the rightmost bin edge

def word_set_pair_corr(w_lst, type_list):

    pair_corr_spacings = []

    length = len(w_lst)

    for w in range(SCAN_WIDTH, len(w_lst)-SCAN_WIDTH):
        #print float(w)/length
        for p in range(w-SCAN_WIDTH, w + SCAN_WIDTH + 1):
            if w != p:
                if w_lst[w] in type_list and w_lst[p] in type_list:
                    if w_lst[w] == w_lst[p]:
                        pair_corr_spacings.append(abs(w-p))

    return np.histogram(pair_corr_spacings, bins=range(SCAN_WIDTH+2), density=True)  # the +2 is because the we're
                                                                                     # defining the rightmost bin edge


full_list = make_word_list('/Users/jmcrook/Desktop/Txt/MBDK.txt')  # Moby Dick

#'/Users/jmcrook/Desktop/Txt/MBDK.txt'

pair_corr1 = get_pair_corr_fast(full_list[:len(full_list)/2])

pair_corr2 = get_pair_corr_fast(full_list[len(full_list)/2:])


print "first half of MBDK"
print pair_corr1

print "second half of MBDK"
print pair_corr2

y1 = [y for y in pair_corr1[0]]
x1 = [int(x) for x in pair_corr1[1][:-1]]

y2 = [y for y in pair_corr2[0]]
x2 = [int(x) for x in pair_corr2[1][:-1]]


pl.plot(x1, y1)
pl.show()

pl.plot(x2, y2)
pl.show()




