__author__ = 'jmcrook'
from random import randint
import pylab as pl
import numpy as np
import time

SCAN_WIDTH = 15


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

full_list = make_word_list('/Users/jmcrook/Desktop/Txt/MBDK.txt')  # a text file of Moby Dick on my desktop


def unigram_modeler(txt): # txt must be word list

    unigram = []
    s = time.time()
    for i in range(10000000):
        r = randint(0, len(txt)-1)
        unigram.append(txt[r])
    e = time.time()
    print "it took " + str(e-s) + "seconds to make the model"
    return unigram


def bigram_modeler(txt2):

    bigram = [txt2[randint(0, len(txt2)-1)]]  # starts the model with a word chosen at random
    for c in range(1000):
        b = [l for l in range(len(txt2)-1) if txt2[l] == bigram[c]]  # gets all indexes of current word
        bigram.append(txt2[b[randint(0, len(b)-1)]+1])  # randomly chooses one of the indexes, adds following word
        print float(c)/len(txt2)

    return bigram


def trigram_modeler(txt2):

    trigram = [txt2[randint(0, len(txt2)-1)]]  # starts the model with a word chosen at random
    b = [l for l in range(len(txt2)-1) if txt2[l] == trigram[0]]  # gets all indexes of current word
    trigram.append(txt2[b[randint(0, len(b)-1)]+1])  # randomly chooses one of the indexes, adds following word

    for c in range(10000):
        s = [q for q in range(len(txt2)-1) if txt2[q] == trigram[c] and txt2[q+1] == trigram[c+1]]  # gets bigram indexes
        trigram.append(txt2[s[randint(0, len(s)-1)]+2])  # randomly chooses one of the indexes, adds following word
        print float(c)/1000

    return trigram


def fourgram_modeler(txt2): # doesn't work

    fourgram = [txt2[randint(0, len(txt2)-1)]]  # starts the model with a word chosen at random
    b = [l for l in range(len(txt2)-1) if txt2[l] == fourgram[0]]  # gets all indexes of current word
    fourgram.append(txt2[b[randint(0, len(b)-1)]+1])  # randomly chooses one of the indexes, adds following word
    s = [q for q in range(len(txt2)-2) if txt2[q] == fourgram[0] and txt2[q+1] == fourgram[1]]  # gets bigram indexes
    fourgram.append(txt2[s[randint(0, len(s)-1)]+2])  # randomly chooses one of the indexes, adds third word

    for c in range(1000):
        f = [g for g in range(len(txt2)-3)
             if txt2[g] == fourgram[c] and txt2[g+1] == fourgram[c+1] and txt2[g+2] == fourgram[c+2]]  # trigram indices
        fourgram.append(txt2[f[randint(0, len(s)-1)]+3])  # randomly chooses one of the indexes, adds 3 away word
        print float(c)/1000

    return fourgram


def bigram_modeler2(txt3, model_len):  # uses tuples, weighted draw from dictionary method
                                       # faster than bigram_modeler for large corpora

    bigram_counts = {}
    draw_dicts = {}
    t1 = time.time()

    for t in range(len(txt3)-1):
     #   print float(t)/len(txt3)

        if tuple(txt3[t:t+2]) not in bigram_counts:
            bigram_counts[tuple(txt3[t:t+2])] = 1
        else:
            bigram_counts[tuple(txt3[t:t+2])] += 1

    model3 = [txt3[randint(0, len(txt3)-1)]]

    for b in range(model_len):
     #   print b/float(model_len), "\n"
        if model3[b] not in draw_dicts:
            draw_dict = {k: v for k, v in bigram_counts.items() if k[0] == model3[b]}
            model3.append(weighted_draw_from_dict(draw_dict))
            draw_dicts[model3[b]] = draw_dict
# this if statement makes it so the modeler doesn't have to rebuild draw_dict for words it's seen before
        else:
            model3.append(weighted_draw_from_dict(draw_dicts[model3[b]]))
    t2 = time.time()

    return model3, t2-t1


def weighted_draw_from_dict(choice_dict):
    """Randomly choose a key from a dict, where the values are the relative probability weights."""
    # http://stackoverflow.com/a/3679747/86684
    choice_items = choice_dict.items()
    total = sum(w for c, w in choice_items)
    r = randint(0, total-1)
    upto = 0
    for c, w in choice_items:
        upto += w
        if upto > r:
            try:
                return c[1]  # this modification requires tuples
            except IndexError:
                print c

    assert False, "Shouldn't get here"


def get_pair_corr_fast(w_lst3): # returns the pair correlation function for all words

    s1 = time.time()
    pair_corr_spacings = []

    length = len(w_lst3)

    for w in range(SCAN_WIDTH, len(w_lst3)-SCAN_WIDTH):
        print float(w)/length
        for p in range(w-SCAN_WIDTH, w + SCAN_WIDTH + 1):
            if w != p:
                if w_lst3[w] == w_lst3[p]:
                    pair_corr_spacings.append(abs(w-p))

    s2 = time.time()
    print "it took " + str(s2-s1) + " seconds to run the pairwise analysis"
    return np.histogram(pair_corr_spacings, bins=range(SCAN_WIDTH+2), density=True)  # the +2 is because the we're
                                                                                   # defining the rightmost bin edge

#print bigram_modeler2(full_list[:2000])

p_model, model_time = bigram_modeler2(full_list, 1000000)
pair_corr = get_pair_corr_fast(p_model)

print(pair_corr)

print "it took " + str(model_time) + " seconds to build the model"

y1 = [y for y in pair_corr[0]]
x1 = [int(x) for x in pair_corr[1][:-1]]


pl.plot(x1, y1)
pl.show()

