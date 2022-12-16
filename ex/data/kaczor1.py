# -*- coding: utf-8 -*-

from books import *

class kaczor1(book):

    def __init__(self):
        super(kaczor1, self).__init__()

        self.src = "/home/cytu/usr/doc/math/ex/Kaczor W., Nowak M. Problems in Mathematical Analysis I Real Numbers Sequences and Series.djvu"
        self.pgs = range(15, 393)
        self.morph0 = 'c150.10' 

        self.tokens.update({
            'sol_start': {'class': 'allbx',
                          'ocr': r'^Solutions$'
                         },
            
            'prob_start': {'class': 'allbx',
                           'ocr': r'^Problems$'
                        },

            'section': {'class': 'allbx',      
                        'ocr': r'^(\d+\.\d+\.) ', 
                        },

            'prob_sol': {'class': 'allbx',      
                         'ocr': r'^(\d+\.\d+\.\d+)\.?',  
                         },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 

        if tk in ['prob_sol']:
            d['k'] = k 
        else:
            if tk in ['prob_start', 'sol_start']:
                d['q_or_a'] = 'a' if tk == 'sol_start' else 'q'
            b_skip = True 

        return b_skip, d
    
    def ym(self, bx):
        bxs = self.bxs(bx)
        foot = list(myset(bxs.line(w=(0.06, 0.1))))
        return self.ymin_line(bx), sort_y(foot)[0][1] if foot else sys.maxsize 
