def groups():
    def replace(s):
        for r in [('“', '"'), ('?”', '"?'), ('”', '"'), ('…', '...'), ('’', "'")]: 
            s = s.replace(*r)
        return s

    return [s.strip() + '?' for s in replace(open('/home/clarktu/usr/doc/lang/txt/4000q.txt', 'r').read()).split('?')]

open('/home/clarktu/Downloads/4000q.txt', 'w').write('\n\n'.join(groups()))
