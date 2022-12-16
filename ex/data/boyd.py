# -*- coding: utf-8 -*-

from books import *

class boyd(book):

    def __init__(self):
        super(boyd, self).__init__()

        self.src = '/home/cytu/usr/doc/math/or/Boyd/Boyd S., Vandenberghe L. Convex Optimization.pdf'

        self.pgs = range(14, 698)
        self.range_linew = (0.84, 0.86)

        self.tokens.update({
            'chapter':  {'class': 'top', 
                         'ocr': r'^Chapter (\d+)$',
                        },

            'section':  {'class': 'allbx', 
                         'ocr': r'^(\d+\.\d+(\.\d+)?) ',
                        },
            
            'bib': {'class': 'allbx',      
                    'ocr': r'^Bibliography$',
                   },
            
            'ex_start': {'class': 'allbx',      
                         'ocr': r'^Exercises$',
                        },
            
            'example': {'class': 'allbx',      
                        'ocr': r'^(Example (\d+\.\d+))',
                       },
            
            'remark': {'class': 'allbx',      
                        'ocr': r'^(Remark (\d+\.\d+))',
                       },

            'bar': {'class': 'line',},

        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        if tk in ['thm', 'proof']:
            if tk == 'thm':
                d['q_or_a'] = 'q'
                d['k'] = k
            else:
                d['q_or_a'] = 'a'
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_line(bx, w=(0.9, 1.0)), sys.maxsize 

    def post(self, d):
        #tkd = d['tkd']
        #is_ex = False
        #for pg in tkd:
        #    l_kill = []
        #    for tk in sorted(tkd[pg], key=lambda b: b[0][1]):
        #        typ = tk[1]
        #        if typ == 'ex_start':
        #            is_ex = True
        #        elif typ == 'chapter':
        #            is_ex = False
        #        if is_ex and typ == 'section':
        #            l_kill.append(tk)
        #    tkd[pg] = [tk for tk in tkd[pg] if tk not in l_kill] 
        self.post_func(d)
