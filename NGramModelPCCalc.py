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


def bigram_g(book):

    v = sorted(set(book))
    word_dist = MLEProbDist(FreqDist(book))
    bigram_dist = ConditionalProbDist(ConditionalFreqDist(bigrams(MobyDick)), MLEProbDist)

    r_1 = sum([bigram_dist[C].prob(C) * word_dist.prob(C) for C in v])

    r_2 = 0
    
    for w in v:
        for b in v:
            r_2 += bigram_dist[b].prob(w) * bigram_dist[w].prob(b) * word_dist.prob(w)

    r_3 = 0

    for w in v:
        for b in v:
            for d in v:
                r_3 += bigram_dist[d].prob(w) * bigram_dist[b].prob(d) * bigram_dist[w].prob(b) * word_dist.prob(w)

    print r_1, r_2, r_3

bigram_g(MobyDick)







