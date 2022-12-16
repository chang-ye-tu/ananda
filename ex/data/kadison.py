# -*- coding: utf-8 -*-
from books import *

class kadison(book):
    
    def __init__(self):
        super(kadison, self).__init__()
        
        self.pgs = range(16, 399)
        self.src = "/home/cytu/usr/doc/math/anly/th/Kadison R., Ringrose J. Fundamentals of Operator Algebras Volume I Fundamental Theory.djvu"

        self.tokens.update({
            'chapter': {'class': 'first2',      
                     'ocr': r'^CHAPTER',
                    },

            'section': {'class': 'indent1', 
                       'ocr': r'^\d+\.\d+\. ',
                      },

            'def': {'class': 'indent1',      
                    'ocr': r'^((\d+\.\d+\.\d+\.) DEFINITION)', 
                   },

            'remark': {'class': 'indent1',      
                    'ocr': r'^((\d+\.\d+\.\d+\.) REMARK)', 
                   },

            'example': {'class': 'indent1',      
                    'ocr': r'^((\d+\.\d+\.\d+\.) EXAMPLE)', 
                   },

            'thm': {'class': 'indent1',      
                    'ocr': r'^((\d+\.\d+\.\d+\.) (LEMMA|COROLLARY|THEOREM|PROPOSITION))', 
                   },
            
            'proof':  {'class': 'indent1', 
                       'ocr': r'^Pr[o0][o0]f.',
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
