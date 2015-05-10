__author__ = 'jmcrook'

for i in range(1, 101):
    line = [str(i), "Crackle", "Pop", True, False, False]
    if i % 3 == 0:
        line[3:5] = [False, True]
    if i % 5 == 0:
        line[3:6] = [False, line[4], True]
    print "".join([line[l] for l in range(3) if line[l+3] is True])
