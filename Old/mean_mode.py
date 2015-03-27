import nltk
import numpy as np
import pylab as pl
import math
import matplotlib
from matplotlib import pyplot
from collections import Counter


def make_word_list(filepath):

    txt_file = open(filepath, 'r')
    txt = txt_file.read()

    txt_chars = [c.lower() for c in txt if (c.isalpha() or c.isspace())]

    for i in range(len(txt_chars)-1):
        if txt_chars[i].isspace():
            if txt_chars[i+1].isspace():
                txt_chars[i] = ''

    new_txt = ''.join((''.join(txt_chars)).splitlines())

    word_list = new_txt.split(' ')

    return word_list


def get_spacings(w_lst1, word):

    spacings = []

    for w in range(len(w_lst1)):
        if w_lst1[w] == word:
            count = 0
            for i in range(len(w_lst1) - (w + 1)):
                if w_lst1[w+1+i] == word:
                    spacings.append(count)
                    count = 0
                else:
                    count += 1

    return spacings


def graph_mean_modes(w_lst2):

    words = []
    means = []
    modes = []

    for l in set(w_lst2):
        w_spacings = [np.log(v) for v in get_spacings(w_lst2, l)]

        if len(w_spacings) != 0:
            words.append(l)
            means.append((sum(w_spacings)/float(len(w_spacings))))
            data = Counter(w_spacings)
            modes.append(data.most_common(1)[0][0])

#    zipped = zip(means, modes, words)

#    zipped2 = [(zipped[g][0], zipped[g][2], zipped[g][2]) for g in range(len(zipped)) if zipped[g][1] != 0]

#    means1 = [zipped[f][0] for f in range(len(zipped2))]
#    means1 = [zipped[f][1] for f in range(len(zipped2))]
#    words1 = [zipped[f][2] for f in range(len(zipped2))]

#    pl.plot(means, modes, 'ro')
#    pl.show()

    for i in range(len(words)):
        matplotlib.pyplot.text(means[i], modes[i], words[i])
    matplotlib.pyplot.show()

kjb = make_word_list('/Users/jmcrook/PycharmProjects/Word Spacings Project/KJB_clean.txt')

graph_mean_modes(kjb[:1200])






