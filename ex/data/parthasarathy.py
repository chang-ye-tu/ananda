# -*- coding: utf-8 -*-
from books import *

class parthasarathy(book):
    
    def __init__(self):
        super(parthasarathy, self).__init__()
        
        self.pgs = range(10, 277)
        self.src = "/home/cytu/usr/doc/math/prob/th/Parthasarathy K. Probability Measures on Metric Spaces.djvu"

        self.tokens.update({
            'chapter': {'class': 'first2',      
                     'ocr': r'^(X|V|I)+',
                    },

            'section': {'class': 'allbx', 
                       'ocr': r'^\d+\. ',
                      },

            'defn': {'class': 'indent0',      
                     'ocr': r'^((Deﬁnition|Definition) (\d+\.\d+))',
                    },

            'remark': {'class': 'indent0', 
                       'ocr': r'^REMARK',
                      },
            
            'example': {'class': 'indent0', 
                        'ocr': r'^(Example (\d+\.\d+))',
                       },

            'thm': {'class': 'indent0',      
                    'ocr': r'^((Lemma|Corollary|Theorem|Proposition) (\d+\.\d+))', 
                   },
            
            'proof':  {'class': 'indent0', 
                       'ocr': r'^PR[oO0][oO0]F',
                      },
        })

    @staticmethod
    def tk_action(ltk, d):
        tk, k = ltk
        b_skip = False 
        
        if tk == 'thm':
            d['q_or_a'] = 'q'
            d['k'] = ' '.join([d['root'], k])
        
        elif tk == 'proof':
            d['q_or_a'] = 'a'

        else:
            if tk == 'chapter':
                d['root'] = k
            b_skip = True
        
        return b_skip, d

    def ym(self, bx):
        bxs = self.bxs(bx)
        nr = list(myset([sort_y(bx)[-1]]) & myset(bxs.centerh()) & myset(bxs.tiny()))
        ml = self.ymax_line(bx)
        return 0 if nr else self.ymin_line(bx), min(sort_y(nr)[-1][1], ml) if nr else ml 
