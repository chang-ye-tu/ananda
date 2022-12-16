def groups():
    def replace(s):
        for r in [('“', '"'), ('?”', '"?'), ('”', '"'), ('…', '...'), ('’', "'")]: 
            s = s.replace(*r)
        return s

    return [s.strip() + '?' for s in replace(open('/home/cytu/usr/doc/lang/txt/4000q.txt', 'r').read()).split('?')]

open('/home/cytu/Downloads/4000q.txt', 'w').write('\n\n'.join(groups()))
