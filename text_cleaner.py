__author__ = 'jmcrook'

import nltk

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



chaps = open('/Users/macadmin/PycharmProjects/spring15/Spring15-master/chapters', 'r')
MobyDick = (open('/Users/macadmin/PycharmProjects/spring15/Spring15-master/MBDK_clean.txt', "r").read()).split(' ')


chapters = []

contents = []

for l in chaps.readlines():
    string = ''
    for c in l:
        if c.isalpha() or c == ' ':
            string += c.lower()
    chapters.append(string)

for P in chapters:
    print P


for i in range(len(MobyDick)):
    if MobyDick[i] == 'chapter':
        name = ''.join(MobyDick[i:i+17])
        for f in chapters:
            if name.startswith(f.replace(' ', '')):
                contents.append((f, i))

print contents


"""
('chapter loomings', 0)
('chapter the spouter inn', 3703)
('chapter the counterpane', 9707)
('chapter breakfast', 11384)
('chapter the street', 12138)
('chapter the pulpit', 13920)
('chapter the sermon', 14891)
('chapter a bosom friend', 18536)
('chapter nightgown', 20107)
('chapter biographical', 20841)
('chapter wheelbarrow', 21733)
...

"""