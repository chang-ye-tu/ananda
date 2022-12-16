# -*- coding: utf-8 -*-

from books import *

class rosenthal_sol(book):
    
    def __init__(self):
        super(rosenthal_sol, self).__init__()
        
        self.pgs = range(6, 89)
        self.morph0 = 'c150.6'

        self.src = u"/home/cytu/usr/doc/math/prob/th/Soltanifar M., Li L.-H., Rosenthal J. A Collection of Exercises in Advanced Probability Theory.pdf"

        self.tokens.update({
            'chap': {'class': 'first2',      
                     'ocr': r'^Chapter ', 
                    },

            'ex': {'class': 'indent0',      
                   'ocr': r'^(Exercise ((\d+|[A])\.\d+\.\d+))', 
                   },

            'sol': {'class': 'indent0',      
                    'ocr': r'^Solution\.', 
                      },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['ex', 'sol']:
            if tk in ['ex']:
                d['q_or_a'] = 'q'
                d['k'] = k.strip()
            else:
                d['q_or_a'] = 'a'
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        return self.ymin_line(bx, w=(0.9, 1.1)), sys.maxsize
