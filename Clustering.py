import nltk
import numpy as np
import sklearn.cluster as cluster
#import pylab as pl
from nltk.probability import *


SCAN_WIDTH = 12

MobyDick = (open('/Users/jmcrook/PycharmProjects/Spring15/MBDK_clean.txt', "r").read()).split(' ')


def word_pair_corr(w_lst, word, density):

    pair_corr_spacings = []
    sw = SCAN_WIDTH

    for w in range(len(w_lst)-sw):
        if w_lst[w] == word:
            for p in range(w+1, w + sw + 1):
                if w_lst[p] == word:
                    pair_corr_spacings.append(p-w)

    hist = [0 for i in range(sw+1)]
    for i in range(1, sw+1):
        for s in pair_corr_spacings:
            if s == i:
                hist[i] += 1

    if density:
        try:
            return [f/float(sum(hist)) for f in hist]
        except ZeroDivisionError:
            return [0 for i in range(SCAN_WIDTH+1)]
    else:
        return hist

MDFreq = FreqDist(MobyDick)
MDCommon = MDFreq.most_common(500)

PCs = [word_pair_corr(MobyDick, c[0], density=True) for c in MDCommon]

clusters = cluster.AgglomerativeClustering(6).fit(PCs)

print clusters.labels_