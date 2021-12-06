import os, codecs, re

def groups():
    s = codecs.open('/home/cytu/usr/doc/lang/txt/boatland.txt', 'r', 'utf-8').read()
    p = re.compile(r'(\d+)\n')

    spans = [m.span() for m in p.finditer(s)]
    pages = [s[spans[i][1] : (spans[i+1][0] if (i < len(spans) - 1) else -1)] for i, c in enumerate(spans)]

    l = []
    for i in range(3, 267):
        l.extend([ss.strip().replace('\n', ' ') for ss in pages[i].split('\n\n') if len(ss.strip()) > 1])

    groups, t = [], {}
    for i, ll in enumerate(l):
        if ll.find(u'–') != -1: # definition
            
            p = re.compile(u'–')
            if len(p.findall(ll)) > 1:
                print ll

            if t:
                groups.append(t)
            t = {'def': ll, 'ex': []}
            
        else:
            t['ex'].append(ll)

    if t:
        groups.append(t)

    return groups
