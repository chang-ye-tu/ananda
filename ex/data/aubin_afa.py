# -*- coding: utf-8 -*-
from books import *

class aubin_afa(book):
    
    def __init__(self):
        super(aubin_afa, self).__init__()
        
        self.pgs = range(18, 461)
        self.src = "/home/cytu/usr/doc/math/anly/th/Aubin/Aubin J.-P. Applied Functional Analysis 2ed.djvu"

        self.tokens.update({
            'section': {'class': 'indent0', 
                       'ocr': r'^\*?(\d+\.\d+\.(\d+\.)?) ',
                      },

            'remark': {'class': 'indent0', 
                       'ocr': r'^\*?(Remark (\d+\.\d+\.\d+))',
                      },
            
            'example': {'class': 'indent0', 
                        'ocr': r'^\*?(Example (\d+\.\d+\.\d+))',
                       },

            'defn': {'class': 'indent0',      
                     'ocr': r'^\*?((Deﬁnition|Definition) (\d+\.\d+\.\d+))',
                    },

            'thm': {'class': 'indent0',      
            'ocr': r'^\*?((Lemma|Corollary|Theorem|Proposition) (\d+\.\d+\.\d+))', 
                   },
            
            'proof':  {'class': 'indent1', 
                       'ocr': r'^Pr[oO0][oO0]f',
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
