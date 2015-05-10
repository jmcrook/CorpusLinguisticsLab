import nltk
import numpy as np
#import pylab as pl
from nltk.probability import *
from nltk.corpus import brown, stopwords


SCAN_WIDTH = 15



            # (chapter name, starting index)
chapters = [('chapter loomings', 0), ('chapter the carpetbag', 2246), ('chapter the spouter inn', 3703), ('chapter the counterpane', 9707), ('chapter breakfast', 11384), ('chapter the street', 12138), ('chapter the pulpit', 13920), ('chapter the sermon', 14891), ('chapter a bosom friend', 18536), ('chapter nightgown', 20107), ('chapter biographical', 20841), ('chapter wheelbarrow', 21733), ('chapter nantucket', 23465), ('chapter chowder', 24231), ('chapter the ship', 25448), ('chapter the ramadan', 31063), ('chapter his mark', 33411), ('chapter the prophet', 34805), ('chapter all astir', 36066), ('chapter going aboard', 37003), ('chapter merry christmas', 38107), ('chapter the lee shore', 39787), ('chapter the advocate', 40162), ('chapter postscript', 41835), ('chapter knights and squires', 42122), ('chapter knights and squires', 42122), ('chapter knights and squires', 43356), ('chapter knights and squires', 43356), ('chapter ahab', 45060), ('chapter enter ahab to him stubb', 46481), ('chapter the pipe', 47729), ('chapter queen mab', 48023), ('chapter cetology', 48912), ('chapter the specksynder', 54115), ('chapter the cabintable', 55100), ('chapter the cabin', 55100), ('chapter the masthead', 57352), ('chapter the quarterdeck', 59988), ('chapter sunset', 62838), ('chapter dusk', 63366), ('chapter first nightwatch', 63767), ('chapter midnight forecastle', 64053), ('chapter moby dick', 65697), ('chapter the whiteness of the whale', 69508), ('chapter hark', 73169), ('chapter the chart', 73489), ('chapter the affidavit', 75554), ('chapter surmises', 79128), ('chapter the matmaker', 80136), ('chapter the first lowering', 81077), ('chapter the hyena', 85122), ('chapter ahab', 85970), ('chapter ahabs boat and crew fedallah', 85970), ('chapter the spiritspout', 87001), ('chapter the albatross', 88530), ('chapter the gam', 89259), ('chapter the townhos story', 90918), ('chapter of the monstrous pictures of whales', 99026), ('chapter of the less erroneous pictures of whales and the true pictures of whaling scenes', 100946), ('chapter brit', 103255), ('chapter squid', 104269), ('chapter the line', 105205), ('chapter stubb kills a whale', 106700), ('chapter the dart', 108700), ('chapter the crotch', 109275), ('chapter stubbs supper', 109752), ('chapter the whale as a dish', 112836), ('chapter the shark massacre', 113843), ('chapter cutting in', 114483), ('chapter the blanket', 115228), ('chapter the funeral', 116440), ('chapter the sphynx', 116886), ('chapter the jeroboams story', 117783), ('chapter the monkeyrope', 120100), ('chapter stubb and flask kill a right whale and then have a talk over him', 121780), ('chapter the sperm whales head  contrasted view', 124022), ('chapter the right whales head  contrasted view', 125690), ('chapter the batteringram', 126943), ('chapter the great heidelburgh tun', 127823), ('chapter cistern and buckets', 128472), ('chapter the prairie', 130148), ('chapter the nut', 131099), ('chapter the pequod meets the virgin', 132015), ('chapter jonah historically regarded', 137640), ('chapter pitchpoling', 138433), ('chapter the fountain', 139250), ('chapter the tail', 141336), ('chapter the grand armada', 143200), ('chapter schools and schoolmasters', 148009), ('chapter fastfish and loosefish', 149208), ('chapter heads or tails', 150656), ('chapter the pequod meets the rosebud', 151720), ('chapter ambergris', 154316), ('chapter the castaway', 155299), ('chapter a squeeze of the hand', 156949), ('chapter the cassock', 158244), ('chapter the tryworks', 158748), ('chapter the lamp', 160594), ('chapter stowing down and clearing up', 160843), ('chapter the doubloon', 161882), ('chapter leg and arm the pequod of nantucket meets the samuel enderby of london', 164412), ('chapter the decanter', 167211), ('chapter a bower in the arsacides', 168972), ('chapter measurement of the whales skeleton', 170558), ('chapter the fossil whale', 171497), ('chapter does the whales magnitude diminish  will he perish', 172938), ('chapter ahab', 174518), ('chapter ahabs leg', 174518), ('chapter the carpenter', 175462), ('chapter ahab', 176531), ('chapter ahab', 178181), ('chapter ahab and starbuck in the cabin', 178181), ('chapter queequeg in his coffin', 179118), ('chapter the pacific', 181406), ('chapter the blacksmith', 181836), ('chapter the forge', 182789), ('chapter the gilder', 184053), ('chapter the dying whale', 185619), ('chapter the whale watch', 186145), ('chapter the quadrant', 186627), ('chapter the candles', 187541), ('chapter the deck', 190127), ('chapter midnight  the forecastle bulwarks', 190322), ('chapter midnight aloft  thunder and lightning', 190976), ('chapter the musket', 191031), ('chapter the needle', 192305), ('chapter the log and line', 193531), ('chapter the lifebuoy', 194679), ('chapter the deck', 196108), ('chapter the pequod meets the rachel', 196853), ('chapter the cabin', 198293), ('chapter the hat', 198894), ('chapter the pequod meets the delight', 200624), ('chapter the symphony', 201064), ('chapter the chase  first day', 202712), ('chapter the chase  second day', 206355), ('chapter the chase  third day', 209754), ('end', -1)]


common = ['whale', 'one', 'like', 'upon', 'man', 'ahab', 'ship', 'ye', 'old', 'sea']

conj = ['and', 'or', 'but', 'for', 'nor', 'yet', 'so']

NPron = ['he', 'she', 'it', 'they', 'we', 'i', 'you']

APron = ['him', 'her', 'you', 'it', 'us', 'them', 'me']


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


def get_pair_corr_fast(w_lst3, density):



    pair_corr_spacings = []

    for w in range(len(w_lst3)-SCAN_WIDTH):
        for p in range(w+1, w + SCAN_WIDTH + 1):
            if w_lst3[w] == w_lst3[p]:
                pair_corr_spacings.append(abs(w-p))

    hist = [0 for i in range(SCAN_WIDTH)]
    for i in range(1, SCAN_WIDTH):
        for s in pair_corr_spacings:
            if s == i:
                hist[i] += 1

    if density:
        return [f/float(sum(hist)) for f in hist]
    else:
        return hist


def word_set_pair_corr_p(w_lst, type_list): #particularized

    pair_corr_spacings = []

    for w in range(len(w_lst)-SCAN_WIDTH):
        for p in range(w+1, w + SCAN_WIDTH + 1):
            if w != p:
                if w_lst[w] in type_list and w_lst[p] in type_list:
                    if w_lst[w] == w_lst[p]:
                        pair_corr_spacings.append(abs(w-p))

    hist = [0 for i in range(SCAN_WIDTH)]
    for i in range(1, SCAN_WIDTH):
        for s in pair_corr_spacings:
            if s == i:
                hist[i] += 1

    return hist


def word_set_pair_corr_g(w_lst, type_list): #generalized

    pair_corr_spacings = []

    for w in range(len(w_lst)-SCAN_WIDTH):
        for p in range(w+1, w + SCAN_WIDTH + 1):
            if w != p:
                if w_lst[w] in type_list and w_lst[p] in type_list:
                    pair_corr_spacings.append(abs(w-p))

    hist = [0 for i in range(SCAN_WIDTH)]
    for i in range(1, SCAN_WIDTH):
        for s in pair_corr_spacings:
            if s == i:
                hist[i] += 1

    return hist


def word_pair_corr(w_lst, word):

    pair_corr_spacings = []
    mcs = get_word_most_common_space(w_lst, word)
    print mcs
    SW = SCAN_WIDTH * mcs

    for w in range(len(w_lst)-SW):
        if w_lst[w] == word:
            for p in range(w+1, w + SW + 1):
                if w_lst[p] == word:
                    pair_corr_spacings.append(p-w)

    hist = [0 for i in range(SW+1)]
    for i in range(1, SW+1):
        print i
        for s in pair_corr_spacings:
            if s == i:
                hist[i] += 1

    return hist


def get_word_most_common_space(w_lst, word):

    spacings = []

    for w in range(len(w_lst)):
        if w_lst[w] == word:
            for p in range(w+1, len(w_lst)):
                if w_lst[p] == word:
                    spacings.append(p-w)
                    break

    return FreqDist(spacings).most_common(1)[0][0]

def get_spacing_density(w_lst):

    spacings = []

    indices = []

    length = len(w_lst)

    for w in range(length-SCAN_WIDTH):
        for p in range(w+1, w + SCAN_WIDTH + 1):
            if w_lst[w] == w_lst[p]:
                indices.append((w, p))
    print 2

    indlen = len(indices)

    for i in range(len(indices)):
        inner = True
        for d in range(i+1, len(indices)):
            if indices[i][1] > indices[d][1]:
                inner = False
                break
        if inner:
            spacings.append(indices[i][1] - indices[i][0])

    return FreqDist(spacings).most_common(30), spacings


# END OF METHODS




"""
MobyDick = (open('/Users/macadmin/PycharmProjects/spring15/Spring15-master/MBDK_clean.txt', "r").read()).split(' ')


mt = open('/Users/macadmin/PycharmProjects/spring15/Spring15-master/MBDK_tagged.txt', "r").read()[2:-2].split('), (')

mt2 = [tuple(c.split(', ')) for c in mt]
mt3 = [(a[1:-1], b[1:-1]) for a, b in mt2]

# print mt3[:5]
# ('chapter', 'NN'), ('loomings', 'NNS'), ('call', 'VBP'), ('me', 'PRP'), ('ishmael', 'VBP')]

MobyTags = [b for a, b in mt3]

print word_set_pair_corr_g(MobyTags, ['JJ', 'JJR', 'JJS'])

get_pair_corr_fast(MobyDick[:(len(MobyDick)/2)])
get_pair_corr_fast(MobyDick[(len(MobyDick)/2):])







stri = 'lazy lazy lazy lazy lazy lazy jane she wants a drink of water so she waits and waits and waits and waits and waits for it to rain w e r t y u i o p l k j h n m b g v f c d x s z'



get_pair_corr_fast(stri.split())

"""

"""
# CHAPTERS

chapterPCs = []

for i in range(len(chapters)-1):
    chapterPCs.append(get_pair_corr_fast(MobyDick[chapters[i][1]:chapters[i+1][1]]))

normPCs = [[] for g in range(len(chapterPCs))]

for P in range(len(chapterPCs)):
    if sum(chapterPCs[P]) != 0:
        sump = sum(chapterPCs[P])
        print sump
        for k in chapterPCs[P]:
            normPCs[P].append(k/float(sump))

for T in normPCs:
    print str(T)[1:-1]

"""


"""

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


"""
