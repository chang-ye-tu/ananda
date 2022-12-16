import os, codecs, unicodedata
from fnmatch import fnmatch

cat = os.path.join
repo = '/home/cytu/usr/doc/lang/txt/'

def fmt(c, d):
    w_min, w_max, w_par = d['w_min'], d['w_max'], d['w_par']
    def no_punc(c):
        sl, tl = [], []
        for line in [li.strip() for li in c.split('\n')]:
            # Discard %% line. 
            if 0 <= line.find('%%') < 2:
                continue

            for s in line:
                try:
                    n = unicodedata.name(s)
                    if 'CJK UNIFIED' in n:# or n == 'SPACE':                
                        tl.append(s)
                    else:                    
                        if tl:
                            sl.append(''.join(tl))
                            tl = []
                except:
                    pass
        if tl:
            sl.append(''.join(tl))
        
        return sl

    sl, tl = [], []
    j = 0

    for i in no_punc(c):
        if len(i) > w_par:
            if tl:
                sl.append('  '.join(tl))
                tl = []
                j = 0
            
            sl.append(i)
            
        else:        
            k = j + len(i)

            if k < w_min:
                tl.append(i)
                j += len(i)
            
            elif w_min <= k:
                if k < w_max:
                    tl.append(i)
                if tl:
                    sl.append('  '.join(tl))
                    tl = []
                    j = 0
                if k >= w_max:
                   tl = [i]
                   j += len(i)
    if tl:               
        sl.append('  '.join(tl))

    return sl

def get_tw_txt():
    fl = []
    for root, dirs, files in os.walk(repo):
        for f in files:
            if fnmatch(f, '*.txt'):
                b = False
                try:
                    ss = codecs.open(cat(root, f), 'r', 'utf-8').read()
                    for s in ss:
                        try:
                            n = unicodedata.name(s)
                            if 'CJK UNIFIED' in n:
                                b = True
                                break
                        except:
                            continue 
                    if b:
                        fl.append(os.path.splitext(os.path.split(f)[1])[0])
                except:
                    'error: ', f 
    return fl

#open('all_txt', 'w').write('\n'.join(get_tw_txt()))

dd = [
    {'n': 'huang', 'w_min': 7, 'w_max': 10, 'w_par': 16},
    {'n': 'chouyi', 'w_min': 6, 'w_max': 12, 'w_par': 12},
    {'n': 'chingjin', 'w_min': 7, 'w_max': 10, 'w_par': 16},
    {'n': 'tao', 'w_min': 5, 'w_max': 12, 'w_par': 12},
    {'n': 'tzuan', 'w_min': 5, 'w_max': 12, 'w_par': 12},
    {'n': 'yi', 'w_min': 5, 'w_max': 12, 'w_par': 12},
    {'n': 'medicine_buddha_sutra', 'w_min': 5, 'w_max': 12, 'w_par': 12},
    {'n': 'sukhavati-vyuha', 'w_min': 5, 'w_max':12 , 'w_par': 16},
    {'n': 'vajra_sutra', 'w_min': 5, 'w_max': 12, 'w_par': 12},
    {'n': 'lotus_sutra', 'w_min': 5, 'w_max': 12, 'w_par': 12},
    {'n': 'ksitigarbha_sutra', 'w_min': 5, 'w_max': 12, 'w_par': 12},
]

for d in dd:
    n = d['n']
    l = ['\n'.join(fmt(bl.strip(), d)) for bl in codecs.open(cat(repo, '%s.txt' % n), 'r', 'utf-8').read().split('\n\n') if bl.strip()]
    codecs.open(cat('/home/cytu/usr/src/py/ananda/tmp/', '%s.txt' % n), 'w', 'utf-8').write('\n\n'.join([ll for ll in l if '\n' in ll]))
