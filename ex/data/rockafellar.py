# -*- coding: utf-8 -*-
from books import *

class rockafellar(book):
    
    def __init__(self):
        super(rockafellar, self).__init__()

        #self.morph_sym = 'c5.3' 
        self.pgs = range(19, 440)
        self.src = "/home/cytu/usr/doc/math/or/Rockafellar/Rockafellar T. Convex Analysis.djvu"

        self.tokens.update({
            'part': {'class': 'first2',      
                     'ocr': r'^PART ',
                    },

            'section': {'class': 'first2', 
                       'ocr': r'^SECTION ',
                      },

            'thm': {'class': 'indent1',      
                    'ocr': r'^((LEMMA|COROLLARY|THEOREM) (\d+\.\d+\.(\d+)?))', 
                   },
            
            'proof':  {'class': 'indent1', 
                       'ocr': r'^PR[O0][O0]F',
                      },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk == 'thm':
            d['q_or_a'] = 'q'
            d['k'] = k 
        
        elif tk == 'proof':
            d['q_or_a'] = 'a'

        else:
            b_skip = True
        
        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        nr = list(myset([sort_y(bx)[-1]]) & myset(bxs.centerh()) & myset(bxs.tiny()))
        ml = self.ymax_line(bx)
        return 0 if nr else self.ymin_line(bx), min(sort_y(nr)[-1][1], ml) if nr else ml 
