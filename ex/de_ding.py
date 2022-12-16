import re, codecs, os, sys

def raw(s):
    # Filter out tags like [ugs.], [Sprw.]
    p = re.compile(r'\[.*?\]')
    return p.sub('', s).strip()

def cmp1(s1, s2):
    return cmp(len(s1), len(s2))

def f(l1, l2):
    l1.sort(cmp1)
    l2.sort(cmp1)
    if len(l1[0]) != len(l2[0]):
        return cmp(len(l1[0]), len(l2[0]))
    return cmp(l1[0], l2[0])    

def mycmp(l1, l2):
    # First extract the de part.
    s1, s2 = raw(l1.split('::')[0]), raw(l2.split('::')[0])
    
    # Note that some parts contain multiple exprs separated by ';'.
    # We should compare the 'minimal' expr.
    return f(s1.split(';'), s2.split(';'))

def ding_sentences():
    q = []
    for s in codecs.open('ding_sentences.txt', 'r', 'utf-8'):
        q.append(s)
    q.sort(mycmp)

    l, t, final_de = [], [], ''
    for s in q:
        de, en = (i.strip(unicode(codecs.BOM_UTF8, 'utf-8')).strip() for i in s.split('::'))
        # Reorder parts with ';'
        des = de.split(';')
        if len(des) > 1:
            des.sort(cmp1)
            de = '; '.join(des)

        if de != final_de:
            if final_de:
                l.append(' :: '.join(['; '.join(t), final_de]))
            t = [en]
        else:
            t.append(en)
        final_de = de
    l.append(' :: '.join(['; '.join(t), final_de]))
    CODE = u'%%  Ding Corpora\n\n%s\n\\begin{itemize}\n%s\n\\end{itemize}'
    ll = [CODE % (k[0], '\n'.join([r'  \item \emph{%s}' % kk for kk in k[1].split('; ')])) for k in (i.split(' :: ') for i in l)]
    return ll
