import nltk
from nltk.book import text1
from nltk.probability import *
from nltk.util import *


txt = [l for l in text1 if l.isalpha()]

bigram_probdist = ConditionalProbDist(
    ConditionalFreqDist(FreqDist(bigrams(txt))), ELEProbDist)


"g(1)"

g_1 = len([c for c in bigrams(txt) if c[0] == c[1]])/float(len(bigrams(txt)))

print g_1


