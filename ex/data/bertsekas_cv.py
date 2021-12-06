# -*- coding: utf-8 -*-

from books import *

class bertsekas_cv(book):

    def __init__(self):
        super(bertsekas_cv, self).__init__()

        self.src = '/home/cytu/usr/doc/math/or/Bertsekas/Convex Analysis and Optimization/convexsolall.pdf'
        self.pgs = range(1, 241)
        self.tokens.update({
            'ex': {'class': 'indent0',      
                   'ocr': r'^(\d+\.\d+)', 
                  },
            
            'sol': {'class': 'indent0',      
                    'ocr': r'^Solution', 
                   },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['sep']:
            b_skip = True

        else:
            if tk == 'sol':
                d['q_or_a'] = 'a'
            else:
                d['k'] = trim(k)
                d['q_or_a'] = 'q' 
        
        return b_skip, d

    def ym(self, bx):
        return 0, self.ymax_skip1(bx) 
