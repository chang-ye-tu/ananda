# -*- coding: utf-8 -*-

from books import *

class mclean(book):
    
    def __init__(self):
        super(mclean, self).__init__()
        
        self.pgs = range(14, 355)

        self.src = "/home/cytu/usr/doc/math/anly/th/McLean W. Strongly Elliptic Systems and Boundary Integral Equations.djvu"
        
        self.tokens.update({
            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem) (\w+\.\d+))', 
                   },
            
            'proof': {'class': 'indent0', 
                      'ocr': r'^Proof',
                     },
            
            'ex_start': {'class': 'indent0',
                         'ocr': r'^Exercises ',
                          },

            'ex': {'class': 'indent0',
                   'ocr': r'^(\w+\.\d+) ',
                    },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk in ['thm', 'proof',]:
            if tk == 'thm':
                d['q_or_a'] = 'q'
                d['k'] = k
            else:
                d['q_or_a'] = 'a'
             
        else:
            b_skip = True

        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        nr = list(myset([sort_y(bx)[-1]]) & myset(bxs.centerh()) & myset(bxs.tiny()))
        ls = bxs.line(w=(0.8, 1))
        y = max(lower(ls)) if ls else min(lower(bx))
        
        ml = self.ymax_line(bx, w=(0.2, 0.4))
        return y if nr else self.ymin_skip1(bx), min(ml, sort_y(nr)[-1][1]) if nr else ml
