__author__ = 'jmcrook'

import nltk
from nltk.probability import *
from nltk.util import bigrams


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

MobyDick = make_word_list('/Users/jmcrook/Desktop/Txt/MBDK.txt')  # Moby Dick


#### unigram model of moby dick

MDFreq = FreqDist(MobyDick)
MDProb = MLEProbDist(MDFreq)

print sum([(MDProb.prob(c) ** 2) for c in set(MobyDick)])
#0.00933926651182
# this is g(r) for all r

#### Bigram model


def bigram_g(r, book):

    bigram_dist = ConditionalProbDist(ConditionalFreqDist(bigrams(book)))

    r_1 = sum([bigram_dist[C].prob(C) for C in set(book)])



