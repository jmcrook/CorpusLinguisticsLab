import nltk
import numpy as np
import pylab as pl
## from nltk.book import *

SCAN_WIDTH = 12


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


full_list = make_word_list('/Users/jmcrook/Desktop/Txt/MBDK.txt')  # Moby Dick

pair_corr = get_pair_corr_fast(full_list)

y1 = [y for y in pair_corr[0]]
x1 = [int(x) for x in pair_corr[1][:-1]]


pl.plot(x1, y1)
pl.show()





