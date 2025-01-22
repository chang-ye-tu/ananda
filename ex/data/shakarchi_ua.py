from books import *

class shakarchi_ua(book):

    def __init__(self):
        super(shakarchi_ua, self).__init__()
        self.src = "/home/cytu/usr/doc/math/alg/Lang/Shakarchi R. Problems and Solutions for Undergraduate Analysis.pdf"
        self.pgs = range(12, 369)
        self.morph0 = 'c150.6'

        self.tokens.update({
            'chapter': {'class': 'first2', 
                        'ocr': r'^(((XX|X{0,1})?(IX|IV|V?I{0,3})?)|0)$',
                       },

            'ex': {'class': 'indent0',      
                   'ocr': '^Exercise \w+\.(\d+\.\d+)', 
                  },

            'sol': {'class': 'indent0',      
                    'ocr': '^[sS]olution\.', 
                   },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['ex', 'sol', ]:
            if tk == 'ex':
                d['q_or_a'] = 'q'
                d['k'] = d.get('root', '0') + '.' + k

            elif tk == 'sol':
                d['q_or_a'] = 'a'

        else:
            if tk == 'chapter':
                d['root'] = k
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_line(bx), self.ymax_line(bx)
