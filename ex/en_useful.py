import os, codecs, random

def useful():
    slist = []
    for i, line in enumerate(codecs.open('/home/cytu/usr/doc/lang/txt/useful.txt', 'r', 'utf-8')):
        #words = line.strip().split()
        #l = len(words)
        #tests = random.sample(range(l), l/2)
        #sl = []
        #for s in range(l):
        #    if s in tests:
        #        sl.append('\\emph{%s}' % words[s])
        #    else:
        #        sl.append(words[s])
        #slist.append(' '.join(sl))
        slist.append(line.strip())
    return slist

