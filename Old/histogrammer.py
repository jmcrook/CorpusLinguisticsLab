import nltk
import numpy as np
import pylab as pl


num_bins = 1000


def make_word_list(filepath):  # turns text file into all lower-case, all alphabetical characters, words split by ' '.

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


def get_spacings(w_lst, word):

    spacings = []

    for w in range(len(w_lst)):
        if w_lst[w] == word:
            count = 0
            for i in range(len(w_lst) - (w + 1)):
                if w_lst[w+1+i] == word:
                    spacings.append(count)
                    count = 0
                else:
                    count += 1

    return spacings


def get_histogram(spacings_list):

    return np.histogram(spacings_list, bins=max(spacings_list), density=True)



kjb = make_word_list('/Users/jmcrook/PycharmProjects/Word Spacings Project/KJB_clean.txt')[:100000]

kjb_spacings = get_spacings(kjb, 'lord')

kjbh = get_histogram(kjb_spacings)

x1 = [x for x in kjbh[1][:-1]]
y1 = [y for y in kjbh[0]]

pl.plot(x1, y1)
pl.show()

#print len(x1), len(y1)

